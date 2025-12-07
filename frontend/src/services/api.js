// API service for connecting to the backend
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/v1';

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  async makeRequest(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;

    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);

      if (!response.ok) {
        // Try to get error details from response
        let errorMessage = `HTTP error! status: ${response.status}`;
        try {
          const errorData = await response.json();
          if (errorData.detail) {
            errorMessage = `${errorMessage} - ${errorData.detail}`;
          }
        } catch (parseError) {
          // If we can't parse the error response, use the status-based message
        }

        throw new Error(errorMessage);
      }

      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);

      // Re-throw a more descriptive error
      if (error instanceof TypeError && error.message.includes('fetch')) {
        throw new Error('Network error: Unable to connect to the API server. Please check your connection.');
      }

      throw error;
    }
  }

  // Query endpoint - general RAG query
  async query(question, userId = null, maxSources = 3) {
    const data = {
      question,
      user_id: userId,
      max_sources: maxSources,
    };

    return this.makeRequest('/query', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Select-query endpoint - selection-only mode
  async selectQuery(selectedText, question, userId = null) {
    const data = {
      selected_text: selectedText,
      question,
      user_id: userId,
    };

    return this.makeRequest('/select-query', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Ingest endpoint - for content ingestion
  async ingest(chapterIds, forceReprocess = false) {
    const data = {
      chapter_ids: chapterIds,
      force_reprocess: forceReprocess,
    };

    return this.makeRequest('/ingest', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Embed endpoint - for generating embeddings
  async embed(chunkIds) {
    const data = {
      chunk_ids: chunkIds,
    };

    return this.makeRequest('/embed', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }
}

export default new ApiService();