import React, { useState, useEffect } from 'react';
import { 
  Settings as SettingsIcon, 
  Mail, 
  Brain, 
  Key,
  Save,
  TestTube,
  AlertCircle
} from 'lucide-react';

const Settings: React.FC = () => {
  const [activeTab, setActiveTab] = useState('general');
  const [saving, setSaving] = useState(false);
  const [testing, setTesting] = useState(false);

  // General settings
  const [autoResponseEnabled, setAutoResponseEnabled] = useState(true);
  const [confidenceThreshold, setConfidenceThreshold] = useState(0.7);
  const [maxEmailsPerFetch, setMaxEmailsPerFetch] = useState(10);

  // Gmail settings
  const [gmailEnabled, setGmailEnabled] = useState(false);
  const [gmailCredentials, setGmailCredentials] = useState('');
  const [gmailLabels, setGmailLabels] = useState('');

  // LLM settings
  const [llmEnabled, setLlmEnabled] = useState(false);
  const [openRouterKey, setOpenRouterKey] = useState('');
  const [selectedModel, setSelectedModel] = useState('meta-llama/llama-2-7b-chat:free');

  const tabs = [
    { id: 'general', name: 'General', icon: SettingsIcon },
    { id: 'gmail', name: 'Gmail Integration', icon: Mail },
    { id: 'llm', name: 'AI Settings', icon: Brain },
  ];

  const handleSave = async () => {
    setSaving(true);
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000));
    setSaving(false);
    // Show success message
  };

  const handleTestGmail = async () => {
    setTesting(true);
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 2000));
    setTesting(false);
    // Show result
  };

  const handleTestLLM = async () => {
    setTesting(true);
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 2000));
    setTesting(false);
    // Show result
  };

  return (
    <div className="p-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Settings</h1>
        <p className="text-gray-600">Configure system parameters and integrations</p>
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 mb-8">
        <div className="border-b border-gray-200">
          <nav className="flex space-x-8 px-6">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`py-4 px-1 border-b-2 font-medium text-sm ${
                    activeTab === tab.id
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <div className="flex items-center space-x-2">
                    <Icon className="w-4 h-4" />
                    <span>{tab.name}</span>
                  </div>
                </button>
              );
            })}
          </nav>
        </div>

        {/* Tab Content */}
        <div className="p-6">
          {/* General Settings */}
          {activeTab === 'general' && (
            <div className="space-y-6">
              <h3 className="text-lg font-medium text-gray-900">General Configuration</h3>
              
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <label className="text-sm font-medium text-gray-700">Enable Auto-Responses</label>
                    <p className="text-sm text-gray-500">Automatically send responses to classified emails</p>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input
                      type="checkbox"
                      checked={autoResponseEnabled}
                      onChange={(e) => setAutoResponseEnabled(e.target.checked)}
                      className="sr-only peer"
                    />
                    <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                  </label>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Confidence Threshold
                  </label>
                  <div className="flex items-center space-x-4">
                    <input
                      type="range"
                      min="0"
                      max="1"
                      step="0.1"
                      value={confidenceThreshold}
                      onChange={(e) => setConfidenceThreshold(parseFloat(e.target.value))}
                      className="w-32"
                    />
                    <span className="text-sm text-gray-600">{Math.round(confidenceThreshold * 100)}%</span>
                  </div>
                  <p className="text-sm text-gray-500 mt-1">
                    Only send auto-responses when confidence is above this threshold
                  </p>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Max Emails Per Fetch
                  </label>
                  <input
                    type="number"
                    min="1"
                    max="50"
                    value={maxEmailsPerFetch}
                    onChange={(e) => setMaxEmailsPerFetch(parseInt(e.target.value))}
                    className="w-32 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                  <p className="text-sm text-gray-500 mt-1">
                    Maximum number of emails to fetch from Gmail in one batch
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Gmail Settings */}
          {activeTab === 'gmail' && (
            <div className="space-y-6">
              <h3 className="text-lg font-medium text-gray-900">Gmail Integration</h3>
              
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <label className="text-sm font-medium text-gray-700">Enable Gmail Integration</label>
                    <p className="text-sm text-gray-500">Connect to Gmail for automatic email fetching</p>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input
                      type="checkbox"
                      checked={gmailEnabled}
                      onChange={(e) => setGmailEnabled(e.target.checked)}
                      className="sr-only peer"
                    />
                    <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                  </label>
                </div>

                {gmailEnabled && (
                  <>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Gmail Credentials File
                      </label>
                      <input
                        type="file"
                        accept=".json"
                        onChange={(e) => setGmailCredentials(e.target.files?.[0]?.name || '')}
                        className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
                      />
                      <p className="text-sm text-gray-500 mt-1">
                        Upload your Gmail API credentials JSON file
                      </p>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Gmail Labels
                      </label>
                      <input
                        type="text"
                        value={gmailLabels}
                        onChange={(e) => setGmailLabels(e.target.value)}
                        placeholder="INBOX, UNREAD"
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                      <p className="text-sm text-gray-500 mt-1">
                        Comma-separated list of Gmail labels to monitor
                      </p>
                    </div>

                    <div className="flex items-center space-x-4">
                      <button
                        onClick={handleTestGmail}
                        disabled={testing}
                        className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        <TestTube className="w-4 h-4" />
                        <span>{testing ? 'Testing...' : 'Test Connection'}</span>
                      </button>
                      
                      {gmailCredentials && (
                        <div className="flex items-center space-x-2 text-green-600">
                          <AlertCircle className="w-4 h-4" />
                          <span className="text-sm">Credentials uploaded</span>
                        </div>
                      )}
                    </div>
                  </>
                )}
              </div>
            </div>
          )}

          {/* LLM Settings */}
          {activeTab === 'llm' && (
            <div className="space-y-6">
              <h3 className="text-lg font-medium text-gray-900">AI Language Model Settings</h3>
              
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <label className="text-sm font-medium text-gray-700">Enable LLM Responses</label>
                    <p className="text-sm text-gray-500">Use AI to generate intelligent email responses</p>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input
                      type="checkbox"
                      checked={llmEnabled}
                      onChange={(e) => setLlmEnabled(e.target.checked)}
                      className="sr-only peer"
                    />
                    <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                  </label>
                </div>

                {llmEnabled && (
                  <>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        OpenRouter API Key
                      </label>
                      <div className="relative">
                        <input
                          type="password"
                          value={openRouterKey}
                          onChange={(e) => setOpenRouterKey(e.target.value)}
                          placeholder="sk-or-..."
                          className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        />
                        <Key className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                      </div>
                      <p className="text-sm text-gray-500 mt-1">
                        Your OpenRouter API key for accessing LLM models
                      </p>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Selected Model
                      </label>
                      <select
                        value={selectedModel}
                        onChange={(e) => setSelectedModel(e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      >
                        <option value="meta-llama/llama-2-7b-chat:free">Llama 2 7B (Free)</option>
                        <option value="meta-llama/llama-2-13b-chat:free">Llama 2 13B (Free)</option>
                        <option value="mistralai/mistral-7b-instruct:free">Mistral 7B (Free)</option>
                        <option value="anthropic/claude-3-haiku:free">Claude 3 Haiku (Free)</option>
                      </select>
                      <p className="text-sm text-gray-500 mt-1">
                        Choose the AI model for generating responses
                      </p>
                    </div>

                    <div className="flex items-center space-x-4">
                      <button
                        onClick={handleTestLLM}
                        disabled={testing || !openRouterKey}
                        className="flex items-center space-x-2 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        <TestTube className="w-4 h-4" />
                        <span>{testing ? 'Testing...' : 'Test LLM'}</span>
                      </button>
                      
                      {openRouterKey && (
                        <div className="flex items-center space-x-2 text-green-600">
                          <AlertCircle className="w-4 h-4" />
                          <span className="text-sm">API key configured</span>
                        </div>
                      )}
                    </div>
                  </>
                )}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Save Button */}
      <div className="flex justify-end">
        <button
          onClick={handleSave}
          disabled={saving}
          className="flex items-center space-x-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <Save className="w-4 h-4" />
          <span>{saving ? 'Saving...' : 'Save Settings'}</span>
        </button>
      </div>
    </div>
  );
};

export default Settings; 