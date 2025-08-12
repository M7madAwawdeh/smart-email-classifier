import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

export interface AnalyticsData {
  category_distribution: Record<string, number>;
  average_confidence: Record<string, number>;
  recent_activity: any[];
}

export interface ModelRetrainResponse {
  message: string;
  accuracy: number;
  training_samples: number;
}

class AnalyticsService {
  private api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
      'Content-Type': 'application/json',
    },
  });

  // Get system analytics
  async getAnalytics(): Promise<AnalyticsData> {
    try {
      const response = await this.api.get('/analytics');
      return response.data;
    } catch (error) {
      console.error('Error fetching analytics:', error);
      throw error;
    }
  }

  // Retrain the classification model
  async retrainModel(): Promise<ModelRetrainResponse> {
    try {
      const response = await this.api.post('/model/retrain');
      return response.data;
    } catch (error) {
      console.error('Error retraining model:', error);
      throw error;
    }
  }

  // Get model performance metrics
  async getModelMetrics(): Promise<any> {
    try {
      const response = await this.api.get('/model/metrics');
      return response.data;
    } catch (error) {
      console.error('Error fetching model metrics:', error);
      throw error;
    }
  }

  // Get training data statistics
  async getTrainingDataStats(): Promise<any> {
    try {
      const response = await this.api.get('/model/training-data');
      return response.data;
    } catch (error) {
      console.error('Error fetching training data stats:', error);
      throw error;
    }
  }

  // Export analytics data
  async exportAnalytics(format: 'csv' | 'json' = 'csv'): Promise<Blob> {
    try {
      const response = await this.api.get('/analytics/export', {
        params: { format },
        responseType: 'blob',
      });
      return response.data;
    } catch (error) {
      console.error('Error exporting analytics:', error);
      throw error;
    }
  }

  // Get performance trends over time
  async getPerformanceTrends(days: number = 30): Promise<any> {
    try {
      const response = await this.api.get('/analytics/trends', {
        params: { days },
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching performance trends:', error);
      throw error;
    }
  }

  // Get category-specific analytics
  async getCategoryAnalytics(category: string): Promise<any> {
    try {
      const response = await this.api.get(`/analytics/category/${category}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching category analytics:', error);
      throw error;
    }
  }

  // Get system health status
  async getSystemHealth(): Promise<any> {
    try {
      const response = await this.api.get('/health');
      return response.data;
    } catch (error) {
      console.error('Error fetching system health:', error);
      throw error;
    }
  }
}

export const analyticsService = new AnalyticsService(); 