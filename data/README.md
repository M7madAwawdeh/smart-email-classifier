# 📊 Training Data Directory

This directory contains sample training data for the Smart Email Classifier system.

## 📁 Files

### `training_emails.json`
- **Format**: JSON array of email objects
- **Content**: 15 labeled email examples
- **Categories**: Support, Sales, Complaints, Feedback, General
- **Use**: Primary training dataset for initial model setup

### `training_emails.csv`
- **Format**: CSV with headers
- **Content**: Same data as JSON file
- **Use**: Alternative format for data processing and import

### `extended_training_data.json`
- **Format**: JSON array of email objects
- **Content**: 15 additional labeled email examples (IDs 16-30)
- **Use**: Extended dataset for improved model training

### `load_training_data.py`
- **Purpose**: Python script to load and process training data
- **Features**: 
  - Loads data from all available files
  - Removes duplicates
  - Shows category distribution
  - Creates training examples
  - Saves summary report

## 🎯 Data Structure

Each training example contains:
```json
{
  "id": 1,
  "subject": "Email subject line",
  "body": "Email body content",
  "category": "Support|Sales|Complaints|Feedback|General",
  "confidence": 0.95
}
```

## 📈 Category Distribution

- **Support**: Technical issues, account problems, bug reports
- **Sales**: Pricing inquiries, quotes, partnership opportunities
- **Complaints**: Service issues, billing problems, delivery complaints
- **Feedback**: Feature requests, suggestions, positive feedback
- **General**: General questions, policy inquiries, information requests

## 🚀 Usage

### 1. Load Training Data
```bash
cd data
python load_training_data.py
```

### 2. Use in Backend
```python
from data.load_training_data import load_json_data

# Load training examples
training_data = load_json_data('data/training_emails.json')

# Use with classifier
classifier = EmailClassifier()
for example in training_data:
    classifier.add_training_example(example['text'], example['category'])
```

### 3. Retrain Model
```bash
# Via API
curl -X POST http://localhost:5000/api/model/retrain

# Via Dashboard
# Use the Analytics page to trigger model retraining
```

## 🔄 Adding New Data

### Add New Examples
1. Edit the JSON files or create new ones
2. Follow the same structure as existing examples
3. Ensure categories match the expected values
4. Run `load_training_data.py` to validate

### Custom Categories
To add new categories:
1. Update the classifier service to handle new categories
2. Add response templates in `LLMService`
3. Update the frontend category filters
4. Retrain the model with new data

## 📊 Data Quality

- **Diversity**: Examples cover various business scenarios
- **Realism**: Based on common customer service emails
- **Balance**: Even distribution across categories
- **Clarity**: Clear category assignments with high confidence

## 🧪 Testing

Test the training data:
```bash
# Test classification
curl -X POST http://localhost:5000/api/classify \
  -H "Content-Type: application/json" \
  -d '{
    "email_text": "I need help with my order",
    "email_subject": "Order Issue"
  }'
```

## 📝 Notes

- Confidence scores are simulated for demonstration
- Real training data should come from actual email classifications
- Use feedback loop to continuously improve the model
- Consider data augmentation for better model performance

---

**Next Steps**: Use this data to train your initial model, then collect real user feedback to improve accuracy over time. 