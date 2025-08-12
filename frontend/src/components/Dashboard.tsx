import React, { useState, useEffect } from 'react';
import { 
  Mail, 
  CheckCircle, 
  Clock, 
  TrendingUp,
  RefreshCw,
  Plus,
  Brain
} from 'lucide-react';
import { emailService } from '../services/emailService';
import { analyticsService } from '../services/analyticsService';

interface DashboardStats {
  totalEmails: number;
  classifiedToday: number;
  accuracy: number;
  avgResponseTime: number;
}

interface RecentEmail {
  id: number;
  subject: string;
  category: string;
  confidence: number;
  created_at: string;
}

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats>({
    totalEmails: 0,
    classifiedToday: 0,
    accuracy: 0,
    avgResponseTime: 0
  });
  const [recentEmails, setRecentEmails] = useState<RecentEmail[]>([]);
  const [loading, setLoading] = useState(true);
  const [fetchingEmails, setFetchingEmails] = useState(false);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      const [analyticsData, emailsData] = await Promise.all([
        analyticsService.getAnalytics(),
        emailService.getEmails(1, 5)
      ]);

      // Process analytics data
      const totalEmails = Object.values(analyticsData.category_distribution || {}).reduce((a: any, b: any) => a + b, 0);
      const accuracy = analyticsData.average_confidence ? 
        Object.values(analyticsData.average_confidence).reduce((a: any, b: any) => a + b, 0) / Object.keys(analyticsData.average_confidence).length : 0;

      setStats({
        totalEmails,
        classifiedToday: emailsData.emails.length,
        accuracy: Math.round(accuracy * 100),
        avgResponseTime: 2.5 // Placeholder - would calculate from actual data
      });

      setRecentEmails(emailsData.emails);
    } catch (error) {
      console.error('Error loading dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFetchEmails = async () => {
    try {
      setFetchingEmails(true);
      await emailService.fetchGmailEmails();
      await loadDashboardData(); // Refresh data
    } catch (error) {
      console.error('Error fetching emails:', error);
    } finally {
      setFetchingEmails(false);
    }
  };

  const handleRetrainModel = async () => {
    try {
      await analyticsService.retrainModel();
      // Show success message
    } catch (error) {
      console.error('Error retraining model:', error);
    }
  };

  if (loading) {
    return (
      <div className="p-8">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/4 mb-6"></div>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="h-24 bg-gray-200 rounded"></div>
            ))}
          </div>
          <div className="h-64 bg-gray-200 rounded"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="p-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Dashboard</h1>
        <p className="text-gray-600">Monitor your email classification system and performance</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div className="flex items-center">
            <div className="p-2 bg-blue-100 rounded-lg">
              <Mail className="w-6 h-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Emails</p>
              <p className="text-2xl font-bold text-gray-900">{stats.totalEmails}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div className="flex items-center">
            <div className="p-2 bg-green-100 rounded-lg">
              <CheckCircle className="w-6 h-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Classified Today</p>
              <p className="text-2xl font-bold text-gray-900">{stats.classifiedToday}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div className="flex items-center">
            <div className="p-2 bg-purple-100 rounded-lg">
              <TrendingUp className="w-6 h-6 text-purple-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Accuracy</p>
              <p className="text-2xl font-bold text-gray-900">{stats.accuracy}%</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div className="flex items-center">
            <div className="p-2 bg-orange-100 rounded-lg">
              <Clock className="w-6 h-6 text-orange-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Avg Response</p>
              <p className="text-2xl font-bold text-gray-900">{stats.avgResponseTime}m</p>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 mb-8">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h2>
        <div className="flex flex-wrap gap-4">
          <button
            onClick={handleFetchEmails}
            disabled={fetchingEmails}
            className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {fetchingEmails ? (
              <RefreshCw className="w-4 h-4 animate-spin" />
            ) : (
              <Mail className="w-4 h-4" />
            )}
            <span>{fetchingEmails ? 'Fetching...' : 'Fetch New Emails'}</span>
          </button>

          <button
            onClick={handleRetrainModel}
            className="flex items-center space-x-2 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
          >
            <Brain className="w-4 h-4" />
            <span>Retrain Model</span>
          </button>

          <button className="flex items-center space-x-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700">
            <Plus className="w-4 h-4" />
            <span>Test Classification</span>
          </button>
        </div>
      </div>

      {/* Recent Emails */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">Recent Emails</h2>
        </div>
        <div className="divide-y divide-gray-200">
          {recentEmails.length === 0 ? (
            <div className="px-6 py-8 text-center text-gray-500">
              <Mail className="w-12 h-12 mx-auto mb-4 text-gray-300" />
              <p>No emails classified yet</p>
              <p className="text-sm">Start by fetching emails from Gmail</p>
            </div>
          ) : (
            recentEmails.map((email) => (
              <div key={email.id} className="px-6 py-4 hover:bg-gray-50">
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <h3 className="text-sm font-medium text-gray-900 truncate">
                      {email.subject}
                    </h3>
                    <div className="flex items-center space-x-4 mt-1">
                      <span className={`category-badge category-${email.category.toLowerCase()}`}>
                        {email.category}
                      </span>
                      <span className="text-sm text-gray-500">
                        Confidence: {Math.round(email.confidence * 100)}%
                      </span>
                      <span className="text-sm text-gray-500">
                        {new Date(email.created_at).toLocaleDateString()}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard; 