#!/usr/bin/env python3
"""
Training Data Loader for Smart Email Classifier
Loads sample training data into the system for initial model training
"""

import json
import csv
import os
import sys
from pathlib import Path

# Add backend to path for imports
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

try:
    from models.email_model import Email
    from services.classifier_service import EmailClassifier
    from app import db, app
except ImportError as e:
    print(f"Error importing backend modules: {e}")
    print("Make sure you're running this from the project root directory")
    sys.exit(1)

def load_json_data(file_path):
    """Load training data from JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON file {file_path}: {e}")
        return []

def load_csv_data(file_path):
    """Load training data from CSV file"""
    try:
        data = []
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert confidence to float
                row['confidence'] = float(row['confidence'])
                data.append(row)
        return data
    except Exception as e:
        print(f"Error loading CSV file {file_path}: {e}")
        return []

def create_training_examples(data):
    """Create training examples for the classifier"""
    examples = []
    for item in data:
        # Combine subject and body for training
        text = f"{item['subject']} {item['body']}"
        examples.append({
            'text': text,
            'category': item['category'],
            'confidence': item['confidence']
        })
    return examples

def main():
    """Main function to load training data"""
    print("🧠 Loading Training Data for Smart Email Classifier")
    print("=" * 50)
    
    # Get data directory
    data_dir = Path(__file__).parent
    json_file = data_dir / "training_emails.json"
    csv_file = data_dir / "training_emails.csv"
    extended_file = data_dir / "extended_training_data.json"
    
    # Load all available data
    all_data = []
    
    if json_file.exists():
        print(f"📁 Loading {json_file.name}...")
        data = load_json_data(json_file)
        all_data.extend(data)
        print(f"   Loaded {len(data)} examples")
    
    if csv_file.exists():
        print(f"📁 Loading {csv_file.name}...")
        data = load_csv_data(csv_file)
        all_data.extend(data)
        print(f"   Loaded {len(data)} examples")
    
    if extended_file.exists():
        print(f"📁 Loading {extended_file.name}...")
        data = load_json_data(extended_file)
        all_data.extend(data)
        print(f"   Loaded {len(data)} examples")
    
    if not all_data:
        print("❌ No training data found!")
        return
    
    # Remove duplicates based on id
    unique_data = {item['id']: item for item in all_data}.values()
    all_data = list(unique_data)
    
    print(f"\n📊 Total unique training examples: {len(all_data)}")
    
    # Show category distribution
    categories = {}
    for item in all_data:
        cat = item['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    print("\n📈 Category Distribution:")
    for cat, count in categories.items():
        print(f"   {cat}: {count} examples")
    
    # Create training examples
    training_examples = create_training_examples(all_data)
    
    print(f"\n🎯 Created {len(training_examples)} training examples")
    
    # Save training data summary
    summary = {
        'total_examples': len(training_examples),
        'categories': categories,
        'examples': training_examples[:5]  # Save first 5 as sample
    }
    
    summary_file = data_dir / "training_summary.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Training summary saved to: {summary_file}")
    
    # Instructions for using the data
    print("\n🚀 Next Steps:")
    print("1. Start the backend server: cd backend && python app.py")
    print("2. Use the dashboard to retrain the model with this data")
    print("3. Or call the API endpoint: POST /api/model/retrain")
    
    print("\n✅ Training data loading complete!")

if __name__ == "__main__":
    main() 