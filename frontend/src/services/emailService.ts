import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

export interface Email {
  id: number;
  subject: string;
  body: string;
  category: string;
  confidence: number;
  auto_response?: string;
  gmail_id?: string;
  from_email?: string;
  to_email?: string;
  created_at: string;
  updated_at: string;
}

export interface EmailListResponse {
  emails: Email[];
  total: number;
  pages: number;
  current_page: number;
}

export interface ClassificationResponse {
  classification: {
    category: string;
    confidence: number;
    probabilities?: Record<string, number>;
  };
  auto_response?: string;
  email_id: number;
}

class EmailService {
  private api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
      'Content-Type': 'application/json',
    },
  });

  // Get paginated list of emails
  async getEmails(page: number = 1, perPage: number = 20, category?: string): Promise<EmailListResponse> {
    try {
      const params: any = { page, per_page: perPage };
      if (category) params.category = category;

      const response = await this.api.get('/emails', { params });
      return response.data;
    } catch (error) {
      console.error('Error fetching emails:', error);
      throw error;
    }
  }

  // Classify a single email
  async classifyEmail(emailText: string, emailSubject: string = ''): Promise<ClassificationResponse> {
    try {
      const response = await this.api.post('/classify', {
        email_text: emailText,
        email_subject: emailSubject,
      });
      return response.data;
    } catch (error) {
      console.error('Error classifying email:', error);
      throw error;
    }
  }

  // Update email category (for feedback loop)
  async updateEmailCategory(emailId: number, category: string, confidence: number = 1.0): Promise<void> {
    try {
      await this.api.put(`/emails/${emailId}`, {
        category,
        confidence,
      });
    } catch (error) {
      console.error('Error updating email category:', error);
      throw error;
    }
  }

  // Fetch new emails from Gmail
  async fetchGmailEmails(): Promise<any> {
    try {
      const response = await this.api.post('/gmail/fetch');
      return response.data;
    } catch (error) {
      console.error('Error fetching Gmail emails:', error);
      throw error;
    }
  }

  // Get email by ID
  async getEmailById(emailId: number): Promise<Email> {
    try {
      const response = await this.api.get(`/emails/${emailId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching email:', error);
      throw error;
    }
  }

  // Search emails
  async searchEmails(query: string, page: number = 1, perPage: number = 20): Promise<EmailListResponse> {
    try {
      const response = await this.api.get('/emails', {
        params: {
          page,
          per_page: perPage,
          search: query,
        },
      });
      return response.data;
    } catch (error) {
      console.error('Error searching emails:', error);
      throw error;
    }
  }

  // Get emails by category
  async getEmailsByCategory(category: string, page: number = 1, perPage: number = 20): Promise<EmailListResponse> {
    try {
      const response = await this.api.get('/emails', {
        params: {
          page,
          per_page: perPage,
          category,
        },
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching emails by category:', error);
      throw error;
    }
  }

  // Export emails (CSV)
  async exportEmails(format: 'csv' | 'json' = 'csv'): Promise<Blob> {
    try {
      const response = await this.api.get('/emails/export', {
        params: { format },
        responseType: 'blob',
      });
      return response.data;
    } catch (error) {
      console.error('Error exporting emails:', error);
      throw error;
    }
  }
}

export const emailService = new EmailService(); 