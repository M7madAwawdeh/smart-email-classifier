import os
import pickle
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import torch
from typing import List, Tuple, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailClassifier:
    """Email classification service using BERT"""
    
    def __init__(self, model_path: str = None):
        self.model = None
        self.tokenizer = None
        self.categories = ['Support', 'Sales', 'Complaints', 'Feedback', 'General']
        self.model_path = model_path or 'backend/model/saved_model'
        self.training_data = []
        
        # Load pre-trained model if exists
        self.load_model()
        
        # If no model exists, initialize with default BERT
        if not self.model:
            self.initialize_model()
    
    def initialize_model(self):
        """Initialize BERT model for sequence classification"""
        try:
            logger.info("Initializing BERT model...")
            
            # Use a smaller BERT model for faster inference
            model_name = "distilbert-base-uncased"
            
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(
                model_name,
                num_labels=len(self.categories),
                id2label={i: label for i, label in enumerate(self.categories)},
                label2id={label: i for i, label in enumerate(self.categories)}
            )
            
            logger.info("BERT model initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing model: {e}")
            # Fallback to simple rule-based classification
            self.model = None
    
    def load_model(self):
        """Load saved model from disk"""
        try:
            if os.path.exists(os.path.join(self.model_path, 'model.pkl')):
                with open(os.path.join(self.model_path, 'model.pkl'), 'rb') as f:
                    saved_data = pickle.load(f)
                    self.model = saved_data['model']
                    self.tokenizer = saved_data['tokenizer']
                    self.training_data = saved_data.get('training_data', [])
                logger.info("Model loaded successfully")
                return True
        except Exception as e:
            logger.error(f"Error loading model: {e}")
        return False
    
    def save_model(self):
        """Save model to disk"""
        try:
            os.makedirs(self.model_path, exist_ok=True)
            
            # Save model and tokenizer
            model_data = {
                'model': self.model,
                'tokenizer': self.tokenizer,
                'training_data': self.training_data
            }
            
            with open(os.path.join(self.model_path, 'model.pkl'), 'wb') as f:
                pickle.dump(model_data, f)
            
            logger.info("Model saved successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error saving model: {e}")
            return False
    
    def preprocess_text(self, text: str) -> str:
        """Preprocess email text for classification"""
        if not text:
            return ""
        
        # Basic text cleaning
        text = text.lower().strip()
        
        # Remove common email artifacts
        text = text.replace('\n', ' ').replace('\r', ' ')
        text = ' '.join(text.split())  # Normalize whitespace
        
        # Remove email signatures (common patterns)
        signature_patterns = [
            'best regards', 'sincerely', 'thanks', 'thank you',
            'regards', 'cheers', 'yours truly', 'yours sincerely'
        ]
        
        for pattern in signature_patterns:
            if pattern in text:
                text = text.split(pattern)[0]
                break
        
        return text[:512]  # BERT has a 512 token limit
    
    def classify_email(self, email_text: str, email_subject: str = "") -> Dict:
        """Classify email and return category with confidence"""
        try:
            if not self.model:
                # Fallback to rule-based classification
                return self._rule_based_classification(email_text, email_subject)
            
            # Combine subject and body for classification
            combined_text = f"{email_subject} {email_text}"
            processed_text = self.preprocess_text(combined_text)
            
            # Tokenize input
            inputs = self.tokenizer(
                processed_text,
                truncation=True,
                padding=True,
                max_length=512,
                return_tensors="pt"
            )
            
            # Get predictions
            with torch.no_grad():
                outputs = self.model(**inputs)
                probabilities = torch.softmax(outputs.logits, dim=-1)
                predicted_class = torch.argmax(probabilities, dim=-1).item()
                confidence = probabilities[0][predicted_class].item()
            
            category = self.categories[predicted_class]
            
            return {
                'category': category,
                'confidence': round(confidence, 3),
                'probabilities': {
                    cat: round(prob.item(), 3) 
                    for cat, prob in zip(self.categories, probabilities[0])
                }
            }
            
        except Exception as e:
            logger.error(f"Error in classification: {e}")
            # Fallback to rule-based
            return self._rule_based_classification(email_text, email_subject)
    
    def _rule_based_classification(self, email_text: str, email_subject: str) -> Dict:
        """Fallback rule-based classification"""
        combined_text = f"{email_subject} {email_text}".lower()
        
        # Define keyword patterns for each category
        patterns = {
            'Support': ['help', 'support', 'issue', 'problem', 'error', 'bug', 'broken'],
            'Sales': ['buy', 'purchase', 'order', 'price', 'cost', 'quote', 'sales'],
            'Complaints': ['complaint', 'angry', 'unhappy', 'dissatisfied', 'refund', 'return'],
            'Feedback': ['feedback', 'suggestion', 'improve', 'better', 'experience'],
            'General': ['question', 'inquiry', 'info', 'information', 'ask']
        }
        
        scores = {}
        for category, keywords in patterns.items():
            score = sum(1 for keyword in keywords if keyword in combined_text)
            scores[category] = score
        
        # Get category with highest score
        if max(scores.values()) == 0:
            category = 'General'
            confidence = 0.5
        else:
            category = max(scores, key=scores.get)
            confidence = min(0.8, 0.5 + (scores[category] * 0.1))
        
        return {
            'category': category,
            'confidence': round(confidence, 3),
            'method': 'rule_based'
        }
    
    def add_training_example(self, text: str, category: str):
        """Add training example for model improvement"""
        if category in self.categories:
            self.training_data.append((text, category))
            logger.info(f"Added training example: {category}")
    
    def retrain_model(self, training_data: List[Tuple[str, str]] = None) -> float:
        """Retrain the model with new data"""
        try:
            if training_data:
                self.training_data.extend(training_data)
            
            if len(self.training_data) < 10:
                logger.warning("Not enough training data for retraining")
                return 0.0
            
            logger.info(f"Retraining model with {len(self.training_data)} examples")
            
            # Prepare training data
            texts, labels = zip(*self.training_data)
            label_ids = [self.categories.index(label) for label in labels]
            
            # Split data
            train_texts, val_texts, train_labels, val_labels = train_test_split(
                texts, label_ids, test_size=0.2, random_state=42
            )
            
            # Tokenize data
            train_encodings = self.tokenizer(
                train_texts, 
                truncation=True, 
                padding=True, 
                return_tensors="pt"
            )
            val_encodings = self.tokenizer(
                val_texts, 
                truncation=True, 
                padding=True, 
                return_tensors="pt"
            )
            
            # Create datasets
            train_dataset = EmailDataset(train_encodings, train_labels)
            val_dataset = EmailDataset(val_encodings, val_labels)
            
            # Training arguments
            training_args = TrainingArguments(
                output_dir='./results',
                num_train_epochs=3,
                per_device_train_batch_size=8,
                per_device_eval_batch_size=8,
                warmup_steps=500,
                weight_decay=0.01,
                logging_dir='./logs',
                logging_steps=10,
            )
            
            # Initialize trainer
            trainer = Trainer(
                model=self.model,
                args=training_args,
                train_dataset=train_dataset,
                eval_dataset=val_dataset,
            )
            
            # Train model
            trainer.train()
            
            # Evaluate
            predictions = trainer.predict(val_dataset)
            pred_labels = np.argmax(predictions.predictions, axis=1)
            accuracy = accuracy_score(val_labels, pred_labels)
            
            logger.info(f"Model retrained successfully. Accuracy: {accuracy:.3f}")
            
            # Save updated model
            self.save_model()
            
            return accuracy
            
        except Exception as e:
            logger.error(f"Error retraining model: {e}")
            return 0.0
    
    def is_model_loaded(self) -> bool:
        """Check if model is loaded and ready"""
        return self.model is not None


class EmailDataset(torch.utils.data.Dataset):
    """Custom dataset for email classification"""
    
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels
    
    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item
    
    def __len__(self):
        return len(self.labels) 