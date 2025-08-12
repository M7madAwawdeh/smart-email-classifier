from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emails.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

# Initialize extensions
db = SQLAlchemy(app)
CORS(app)

# Import models and services
from models.email_model import Email
from services.classifier_service import EmailClassifier
from services.gmail_service import GmailService
from services.llm_service import LLMService

# Initialize services
classifier = EmailClassifier()
gmail_service = GmailService()
llm_service = LLMService()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'model_loaded': classifier.is_model_loaded()
    })

@app.route('/api/classify', methods=['POST'])
def classify_email():
    """Classify an email and generate response"""
    try:
        data = request.get_json()
        email_text = data.get('email_text', '')
        email_subject = data.get('email_subject', '')
        
        if not email_text:
            return jsonify({'error': 'Email text is required'}), 400
        
        # Classify email
        classification = classifier.classify_email(email_text, email_subject)
        
        # Generate auto-response if enabled
        auto_response = None
        if classification['confidence'] > 0.7:  # Only auto-respond if confident
            auto_response = llm_service.generate_response(
                email_text, 
                classification['category']
            )
        
        # Store email in database
        email_record = Email(
            subject=email_subject,
            body=email_text,
            category=classification['category'],
            confidence=classification['confidence'],
            auto_response=auto_response
        )
        db.session.add(email_record)
        db.session.commit()
        
        return jsonify({
            'classification': classification,
            'auto_response': auto_response,
            'email_id': email_record.id
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/emails', methods=['GET'])
def get_emails():
    """Get all classified emails with pagination"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        category = request.args.get('category', None)
        
        query = Email.query
        
        if category:
            query = query.filter(Email.category == category)
        
        emails = query.order_by(Email.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'emails': [email.to_dict() for email in emails.items],
            'total': emails.total,
            'pages': emails.pages,
            'current_page': page
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/emails/<int:email_id>', methods=['PUT'])
def update_email_category(email_id):
    """Update email category (for feedback loop)"""
    try:
        data = request.get_json()
        new_category = data.get('category')
        confidence = data.get('confidence', 1.0)
        
        email = Email.query.get_or_404(email_id)
        email.category = new_category
        email.confidence = confidence
        email.updated_at = datetime.now()
        
        db.session.commit()
        
        # Add to training data for model improvement
        classifier.add_training_example(email.body, new_category)
        
        return jsonify({'message': 'Email updated successfully'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    """Get system analytics"""
    try:
        # Category distribution
        category_counts = db.session.query(
            Email.category, 
            db.func.count(Email.id)
        ).group_by(Email.category).all()
        
        # Average confidence by category
        avg_confidence = db.session.query(
            Email.category,
            db.func.avg(Email.confidence)
        ).group_by(Email.category).all()
        
        # Recent activity
        recent_emails = Email.query.order_by(
            Email.created_at.desc()
        ).limit(10).all()
        
        return jsonify({
            'category_distribution': dict(category_counts),
            'average_confidence': dict(avg_confidence),
            'recent_activity': [email.to_dict() for email in recent_emails]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/gmail/fetch', methods=['POST'])
def fetch_gmail_emails():
    """Fetch new emails from Gmail and classify them"""
    try:
        # Fetch unread emails from Gmail
        emails = gmail_service.fetch_unread_emails()
        
        results = []
        for email in emails:
            # Classify each email
            classification = classifier.classify_email(
                email['body'], 
                email['subject']
            )
            
            # Generate response if confident
            auto_response = None
            if classification['confidence'] > 0.7:
                auto_response = llm_service.generate_response(
                    email['body'], 
                    classification['category']
                )
                
                # Send auto-response if enabled
                if auto_response:
                    gmail_service.send_email(
                        to=email['from'],
                        subject=f"Re: {email['subject']}",
                        body=auto_response
                    )
            
            # Store in database
            email_record = Email(
                subject=email['subject'],
                body=email['body'],
                category=classification['category'],
                confidence=classification['confidence'],
                auto_response=auto_response,
                gmail_id=email['id']
            )
            db.session.add(email_record)
            results.append({
                'gmail_id': email['id'],
                'classification': classification,
                'auto_response_sent': bool(auto_response)
            })
        
        db.session.commit()
        
        return jsonify({
            'emails_processed': len(results),
            'results': results
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/model/retrain', methods=['POST'])
def retrain_model():
    """Retrain the classification model with new data"""
    try:
        # Get all labeled emails for training
        emails = Email.query.filter(Email.confidence == 1.0).all()
        
        if len(emails) < 10:
            return jsonify({'error': 'Need at least 10 labeled emails for training'}), 400
        
        # Prepare training data
        training_data = [(email.body, email.category) for email in emails]
        
        # Retrain model
        accuracy = classifier.retrain_model(training_data)
        
        return jsonify({
            'message': 'Model retrained successfully',
            'accuracy': accuracy,
            'training_samples': len(training_data)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(debug=True, host='0.0.0.0', port=5000) 