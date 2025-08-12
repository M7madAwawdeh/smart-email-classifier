from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Email(db.Model):
    """Email model for storing classified emails"""
    
    __tablename__ = 'emails'
    
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(500), nullable=False)
    body = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    confidence = db.Column(db.Float, nullable=False, default=0.0)
    auto_response = db.Column(db.Text, nullable=True)
    gmail_id = db.Column(db.String(100), nullable=True, unique=True)
    from_email = db.Column(db.String(255), nullable=True)
    to_email = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Email {self.id}: {self.subject[:50]}...>'
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'subject': self.subject,
            'body': self.body[:200] + '...' if len(self.body) > 200 else self.body,
            'category': self.category,
            'confidence': round(self.confidence, 3),
            'auto_response': self.auto_response,
            'gmail_id': self.gmail_id,
            'from_email': self.from_email,
            'to_email': self.to_email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def get_categories(cls):
        """Get all unique categories"""
        return [row[0] for row in db.session.query(cls.category).distinct()]
    
    @classmethod
    def get_category_count(cls, category):
        """Get count of emails in a specific category"""
        return cls.query.filter_by(category=category).count()
    
    @classmethod
    def get_recent_emails(cls, limit=10):
        """Get recent emails"""
        return cls.query.order_by(cls.created_at.desc()).limit(limit).all() 