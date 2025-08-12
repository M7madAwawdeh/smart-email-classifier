import os
import httpx
import json
from typing import Dict, Optional
from dotenv import load_dotenv
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMService:
    """LLM service using OpenRouter API for email response generation"""
    
    def __init__(self):
        self.api_key = os.getenv('OPENROUTER_API_KEY')
        self.base_url = "https://openrouter.ai/api/v1"
        self.default_model = "meta-llama/llama-2-7b-chat:free"  # Free tier model
        
        # Response templates for different categories
        self.response_templates = {
            'Support': {
                'system_prompt': """You are a professional customer support representative. 
                Generate a helpful, empathetic response to customer support inquiries. 
                Be specific, offer solutions, and maintain a professional yet friendly tone.""",
                'examples': [
                    "I understand you're experiencing [issue]. Let me help you resolve this...",
                    "Thank you for reaching out about [issue]. Here's what we can do...",
                    "I'm sorry to hear about [issue]. Let me assist you with..."
                ]
            },
            'Sales': {
                'system_prompt': """You are a professional sales representative. 
                Generate an engaging, informative response to sales inquiries. 
                Highlight benefits, provide relevant information, and encourage further engagement.""",
                'examples': [
                    "Thank you for your interest in [product/service]! Here's what makes us special...",
                    "Great question about [product/service]! Let me share the key benefits...",
                    "I'd be happy to help you with [product/service]. Here's what you should know..."
                ]
            },
            'Complaints': {
                'system_prompt': """You are a professional customer service representative handling complaints. 
                Generate an empathetic, apologetic response that acknowledges the issue and shows commitment to resolution. 
                Be understanding and offer concrete next steps.""",
                'examples': [
                    "I sincerely apologize for [issue]. This is not the experience we want you to have...",
                    "I understand your frustration with [issue], and I want you to know we take this seriously...",
                    "Thank you for bringing [issue] to our attention. I'm truly sorry this happened..."
                ]
            },
            'Feedback': {
                'system_prompt': """You are a professional representative responding to customer feedback. 
                Generate a grateful, appreciative response that shows you value their input. 
                Acknowledge their feedback and mention how it helps improve your service.""",
                'examples': [
                    "Thank you so much for taking the time to share your feedback about [topic]...",
                    "We truly appreciate your thoughtful feedback regarding [topic]...",
                    "Your feedback about [topic] is incredibly valuable to us..."
                ]
            },
            'General': {
                'system_prompt': """You are a professional representative responding to general inquiries. 
                Generate a helpful, informative response that addresses their question clearly. 
                Be friendly, professional, and provide useful information.""",
                'examples': [
                    "Thank you for your inquiry about [topic]. Here's what I can tell you...",
                    "Great question! Let me provide you with information about [topic]...",
                    "I'd be happy to help you with information about [topic]..."
                ]
            }
        }
    
    def generate_response(self, email_text: str, category: str, custom_prompt: str = None) -> Optional[str]:
        """Generate an appropriate response based on email category"""
        try:
            if not self.api_key:
                logger.warning("OpenRouter API key not found. Using template responses.")
                return self._generate_template_response(email_text, category)
            
            # Get category-specific template
            template = self.response_templates.get(category, self.response_templates['General'])
            
            # Build the prompt
            if custom_prompt:
                system_prompt = custom_prompt
            else:
                system_prompt = template['system_prompt']
            
            user_prompt = f"""Please generate a professional email response to the following customer email:

Customer Email:
{email_text}

Category: {category}

Requirements:
- Keep the response under 150 words
- Be professional yet friendly
- Address the customer's specific concerns
- Offer helpful solutions or information
- Maintain the appropriate tone for {category} emails

Please provide only the response text, no additional formatting."""
            
            # Call OpenRouter API
            response = self._call_openrouter_api(system_prompt, user_prompt)
            
            if response:
                logger.info(f"Generated {category} response successfully")
                return response
            else:
                logger.warning("OpenRouter API call failed, falling back to template")
                return self._generate_template_response(email_text, category)
                
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return self._generate_template_response(email_text, category)
    
    def _call_openrouter_api(self, system_prompt: str, user_prompt: str) -> Optional[str]:
        """Make API call to OpenRouter"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://smart-email-classifier.com",
                "X-Title": "Smart Email Classifier"
            }
            
            payload = {
                "model": self.default_model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "max_tokens": 300,
                "temperature": 0.7,
                "top_p": 0.9
            }
            
            with httpx.Client(timeout=30.0) as client:
                response = client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data['choices'][0]['message']['content'].strip()
                else:
                    logger.error(f"OpenRouter API error: {response.status_code} - {response.text}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error calling OpenRouter API: {e}")
            return None
    
    def _generate_template_response(self, email_text: str, category: str) -> str:
        """Generate a template-based response when LLM is unavailable"""
        template = self.response_templates.get(category, self.response_templates['General'])
        
        # Simple keyword-based response generation
        email_lower = email_text.lower()
        
        if category == 'Support':
            if any(word in email_lower for word in ['help', 'issue', 'problem']):
                return """Thank you for reaching out. I understand you're experiencing an issue, and I'm here to help resolve it. 

Could you please provide more specific details about what you're encountering? This will help me assist you more effectively.

In the meantime, you might find helpful information in our knowledge base or FAQ section.

Best regards,
Customer Support Team"""
            else:
                return """Thank you for contacting our support team. I'm here to help you with any questions or concerns you may have.

Please let me know how I can assist you today, and I'll do my best to provide a quick and helpful solution.

Best regards,
Customer Support Team"""
        
        elif category == 'Sales':
            if any(word in email_lower for word in ['price', 'cost', 'quote']):
                return """Thank you for your interest in our products/services! I'd be happy to provide you with pricing information and answer any questions you may have.

To give you the most accurate quote, could you share a bit more about your specific needs? This will help me provide you with the best options and pricing.

I'll follow up with detailed information shortly.

Best regards,
Sales Team"""
            else:
                return """Thank you for your inquiry! I'm excited to tell you more about our products/services and how they can benefit you.

I'd love to schedule a brief call to discuss your needs in detail and show you the perfect solution. When would be a convenient time for you?

Best regards,
Sales Team"""
        
        elif category == 'Complaints':
            return """I sincerely apologize for the negative experience you've had. This is not the level of service we strive to provide, and I want you to know we take your feedback very seriously.

I'm committed to resolving this issue for you. Could you please provide additional details so I can investigate and take appropriate action?

I'll personally follow up with you within 24 hours to ensure we address your concerns completely.

Best regards,
Customer Service Manager"""
        
        elif category == 'Feedback':
            return """Thank you so much for taking the time to share your feedback with us! We truly value input from our customers as it helps us continuously improve our products and services.

Your insights are incredibly valuable, and I've shared them with our team for review. We're committed to using this feedback to enhance the customer experience.

We appreciate you being part of our community and helping us grow.

Best regards,
Customer Experience Team"""
        
        else:  # General
            return """Thank you for your inquiry! I'm here to help you with any questions or information you may need.

I'll do my best to provide you with a comprehensive and helpful response. If you need any clarification or have additional questions, please don't hesitate to ask.

Best regards,
Customer Service Team"""
    
    def update_response_template(self, category: str, system_prompt: str, examples: list = None):
        """Update response templates for customization"""
        if category in self.response_templates:
            self.response_templates[category]['system_prompt'] = system_prompt
            if examples:
                self.response_templates[category]['examples'] = examples
            logger.info(f"Updated response template for {category}")
    
    def get_available_models(self) -> list:
        """Get list of available OpenRouter models"""
        try:
            if not self.api_key:
                return []
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            with httpx.Client(timeout=10.0) as client:
                response = client.get(
                    f"{self.base_url}/models",
                    headers=headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return [model['id'] for model in data.get('data', [])]
                else:
                    logger.error(f"Error fetching models: {response.status_code}")
                    return []
                    
        except Exception as e:
            logger.error(f"Error getting available models: {e}")
            return []
    
    def test_connection(self) -> bool:
        """Test OpenRouter API connection"""
        try:
            if not self.api_key:
                return False
            
            # Try to get available models
            models = self.get_available_models()
            return len(models) > 0
            
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False 