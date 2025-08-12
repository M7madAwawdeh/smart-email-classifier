import os
import base64
import email
from typing import List, Dict, Optional
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GmailService:
    """Gmail API service for email operations"""
    
    # Gmail API scopes
    SCOPES = [
        'https://www.googleapis.com/auth/gmail.readonly',
        'https://www.googleapis.com/auth/gmail.send',
        'https://www.googleapis.com/auth/gmail.modify'
    ]
    
    def __init__(self):
        self.service = None
        self.credentials = None
        self.authenticate()
    
    def authenticate(self):
        """Authenticate with Gmail API using OAuth2"""
        try:
            creds = None
            
            # Check if token file exists
            token_path = 'backend/credentials/token.json'
            if os.path.exists(token_path):
                creds = Credentials.from_authorized_user_file(token_path, self.SCOPES)
            
            # If no valid credentials, let user log in
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    # Check if credentials file exists
                    creds_file = 'backend/credentials/credentials.json'
                    if not os.path.exists(creds_file):
                        logger.error("credentials.json not found. Please download from Google Cloud Console")
                        return
                    
                    flow = InstalledAppFlow.from_client_secrets_file(creds_file, self.SCOPES)
                    creds = flow.run_local_server(port=0)
                
                # Save credentials for next run
                os.makedirs('backend/credentials', exist_ok=True)
                with open(token_path, 'w') as token:
                    token.write(creds.to_json())
            
            self.credentials = creds
            self.service = build('gmail', 'v1', credentials=creds)
            logger.info("Gmail authentication successful")
            
        except Exception as e:
            logger.error(f"Gmail authentication failed: {e}")
            self.service = None
    
    def fetch_unread_emails(self, max_results: int = 10) -> List[Dict]:
        """Fetch unread emails from Gmail"""
        try:
            if not self.service:
                logger.error("Gmail service not authenticated")
                return []
            
            # Query for unread emails
            results = self.service.users().messages().list(
                userId='me',
                labelIds=['UNREAD'],
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            emails = []
            
            for message in messages:
                try:
                    email_data = self._get_email_details(message['id'])
                    if email_data:
                        emails.append(email_data)
                except Exception as e:
                    logger.error(f"Error processing email {message['id']}: {e}")
                    continue
            
            logger.info(f"Fetched {len(emails)} unread emails")
            return emails
            
        except HttpError as error:
            logger.error(f"Gmail API error: {error}")
            return []
        except Exception as e:
            logger.error(f"Error fetching emails: {e}")
            return []
    
    def _get_email_details(self, message_id: str) -> Optional[Dict]:
        """Get detailed information about a specific email"""
        try:
            message = self.service.users().messages().get(
                userId='me',
                id=message_id,
                format='full'
            ).execute()
            
            headers = message['payload']['headers']
            
            # Extract email details
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            from_email = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
            to_email = next((h['value'] for h in headers if h['name'] == 'To'), 'Unknown')
            date = next((h['value'] for h in headers if h['name'] == 'Date'), '')
            
            # Extract email body
            body = self._extract_email_body(message['payload'])
            
            return {
                'id': message_id,
                'subject': subject,
                'from': from_email,
                'to': to_email,
                'date': date,
                'body': body,
                'snippet': message.get('snippet', '')
            }
            
        except Exception as e:
            logger.error(f"Error getting email details: {e}")
            return None
    
    def _extract_email_body(self, payload: Dict) -> str:
        """Extract email body from Gmail API payload"""
        try:
            if 'body' in payload and payload['body'].get('data'):
                # Simple text email
                data = payload['body']['data']
                return base64.urlsafe_b64decode(data).decode('utf-8')
            
            elif 'parts' in payload:
                # Multipart email
                for part in payload['parts']:
                    if part['mimeType'] == 'text/plain':
                        if 'data' in part['body']:
                            data = part['body']['data']
                            return base64.urlsafe_b64decode(data).decode('utf-8')
                    elif part['mimeType'] == 'text/html':
                        if 'data' in part['body']:
                            data = part['body']['data']
                            html_content = base64.urlsafe_b64decode(data).decode('utf-8')
                            # Simple HTML to text conversion
                            import re
                            text_content = re.sub('<[^<]+?>', '', html_content)
                            return text_content
            
            return "No readable content found"
            
        except Exception as e:
            logger.error(f"Error extracting email body: {e}")
            return "Error reading email content"
    
    def send_email(self, to: str, subject: str, body: str, reply_to: str = None) -> bool:
        """Send an email via Gmail API"""
        try:
            if not self.service:
                logger.error("Gmail service not authenticated")
                return False
            
            # Create email message
            message = self._create_message(to, subject, body, reply_to)
            
            # Send email
            sent_message = self.service.users().messages().send(
                userId='me',
                body=message
            ).execute()
            
            logger.info(f"Email sent successfully: {sent_message['id']}")
            return True
            
        except HttpError as error:
            logger.error(f"Gmail API error sending email: {error}")
            return False
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return False
    
    def _create_message(self, to: str, subject: str, body: str, reply_to: str = None) -> Dict:
        """Create Gmail API message format"""
        message = email.mime.text.MIMEText(body)
        message['to'] = to
        message['subject'] = subject
        
        if reply_to:
            message['reply-to'] = reply_to
        
        # Encode message
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        
        return {'raw': raw_message}
    
    def mark_as_read(self, message_id: str) -> bool:
        """Mark an email as read"""
        try:
            if not self.service:
                return False
            
            # Remove UNREAD label
            self.service.users().messages().modify(
                userId='me',
                id=message_id,
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
            
            logger.info(f"Marked email {message_id} as read")
            return True
            
        except Exception as e:
            logger.error(f"Error marking email as read: {e}")
            return False
    
    def add_label(self, message_id: str, label_name: str) -> bool:
        """Add a label to an email"""
        try:
            if not self.service:
                return False
            
            # Get or create label
            label_id = self._get_or_create_label(label_name)
            
            # Add label to message
            self.service.users().messages().modify(
                userId='me',
                id=message_id,
                body={'addLabelIds': [label_id]}
            ).execute()
            
            logger.info(f"Added label '{label_name}' to email {message_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding label: {e}")
            return False
    
    def _get_or_create_label(self, label_name: str) -> str:
        """Get existing label or create new one"""
        try:
            # List existing labels
            results = self.service.users().labels().list(userId='me').execute()
            labels = results.get('labels', [])
            
            # Check if label exists
            for label in labels:
                if label['name'] == label_name:
                    return label['id']
            
            # Create new label
            label_object = {
                'name': label_name,
                'labelListVisibility': 'labelShow',
                'messageListVisibility': 'show'
            }
            
            created_label = self.service.users().labels().create(
                userId='me',
                body=label_object
            ).execute()
            
            return created_label['id']
            
        except Exception as e:
            logger.error(f"Error managing labels: {e}")
            return 'INBOX'  # Fallback to inbox
    
    def is_authenticated(self) -> bool:
        """Check if Gmail service is authenticated"""
        return self.service is not None 