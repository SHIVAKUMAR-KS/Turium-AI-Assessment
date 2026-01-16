import React, { useState, useEffect } from 'react'
import axios from 'axios'
import './index.css'

const API_BASE = '/api'

function App() {
  const [activeTab, setActiveTab] = useState('ingest')
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(null)

  // Ingest form state
  const [ingestType, setIngestType] = useState('text')
  const [textContent, setTextContent] = useState('')
  const [urlContent, setUrlContent] = useState('')

  // Query state
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState(null)
  const [sources, setSources] = useState([])
  const [queryLoading, setQueryLoading] = useState(false)

  // Fetch items on mount
  useEffect(() => {
    fetchItems()
  }, [])

  const fetchItems = async () => {
    try {
      setLoading(true)
      const response = await axios.get(`${API_BASE}/items`)
      setItems(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch items')
    } finally {
      setLoading(false)
    }
  }

  const handleIngest = async (e) => {
    e.preventDefault()
    setError(null)
    setSuccess(null)

    try {
      setLoading(true)
      const payload = ingestType === 'text'
        ? { content: textContent }
        : { url: urlContent }

      const response = await axios.post(`${API_BASE}/ingest`, payload)
      
      setSuccess(`Content ingested successfully! Created ${response.data.chunks_count} chunks.`)
      setTextContent('')
      setUrlContent('')
      await fetchItems()
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to ingest content')
    } finally {
      setLoading(false)
    }
  }

  const handleQuery = async (e) => {
    e.preventDefault()
    setError(null)
    setAnswer(null)
    setSources([])

    if (!question.trim()) {
      setError('Please enter a question')
      return
    }

    try {
      setQueryLoading(true)
      const response = await axios.post(`${API_BASE}/query`, {
        question: question.trim()
      })
      
      setAnswer(response.data.answer)
      setSources(response.data.sources)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to process query')
    } finally {
      setQueryLoading(false)
    }
  }

  return (
    <div className="container">
      <h1 style={{ marginBottom: '30px', color: '#2c3e50' }}>
        AI Knowledge Inbox
      </h1>

      <div className="tabs">
        <button
          className={`tab ${activeTab === 'ingest' ? 'active' : ''}`}
          onClick={() => setActiveTab('ingest')}
        >
          Add Content
        </button>
        <button
          className={`tab ${activeTab === 'items' ? 'active' : ''}`}
          onClick={() => setActiveTab('items')}
        >
          Saved Items ({items.length})
        </button>
        <button
          className={`tab ${activeTab === 'query' ? 'active' : ''}`}
          onClick={() => setActiveTab('query')}
        >
          Ask Question
        </button>
      </div>

      {error && <div className="error">{error}</div>}
      {success && <div className="success">{success}</div>}

      {/* Ingest Tab */}
      <div className={`tab-content ${activeTab === 'ingest' ? 'active' : ''}`}>
        <div className="card">
          <h2>Add Content</h2>
          <form onSubmit={handleIngest}>
            <div className="form-group">
              <label>
                <input
                  type="radio"
                  value="text"
                  checked={ingestType === 'text'}
                  onChange={(e) => setIngestType(e.target.value)}
                  style={{ width: 'auto', marginRight: '8px' }}
                />
                Text Note
              </label>
              <label style={{ marginLeft: '20px' }}>
                <input
                  type="radio"
                  value="url"
                  checked={ingestType === 'url'}
                  onChange={(e) => setIngestType(e.target.value)}
                  style={{ width: 'auto', marginRight: '8px' }}
                />
                URL
              </label>
            </div>

            {ingestType === 'text' ? (
              <div className="form-group">
                <label htmlFor="text-content">Text Content</label>
                <textarea
                  id="text-content"
                  value={textContent}
                  onChange={(e) => setTextContent(e.target.value)}
                  placeholder="Enter your note here..."
                  required
                />
              </div>
            ) : (
              <div className="form-group">
                <label htmlFor="url-content">URL</label>
                <input
                  id="url-content"
                  type="url"
                  value={urlContent}
                  onChange={(e) => setUrlContent(e.target.value)}
                  placeholder="https://example.com/article"
                  required
                />
              </div>
            )}

            <button type="submit" className="button" disabled={loading}>
              {loading ? 'Processing...' : 'Add Content'}
            </button>
          </form>
        </div>
      </div>

      {/* Items Tab */}
      <div className={`tab-content ${activeTab === 'items' ? 'active' : ''}`}>
        <div className="card">
          <h2>Saved Items</h2>
          {loading && items.length === 0 ? (
            <div className="loading">Loading items...</div>
          ) : items.length === 0 ? (
            <div className="loading">No items saved yet. Add some content!</div>
          ) : (
            <ul className="item-list">
              {items.map((item) => (
                <li key={item.id} className="item">
                  <div className="item-header">
                    <span className={`item-type ${item.source_type}`}>
                      {item.source_type}
                    </span>
                    <span style={{ fontSize: '12px', color: '#999' }}>
                      {new Date(item.created_at).toLocaleString()}
                    </span>
                  </div>
                  {item.source_url && (
                    <a
                      href={item.source_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="item-url"
                    >
                      {item.source_url}
                    </a>
                  )}
                  <div className="item-content">
                    {item.content.length > 200
                      ? `${item.content.substring(0, 200)}...`
                      : item.content}
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>

      {/* Query Tab */}
      <div className={`tab-content ${activeTab === 'query' ? 'active' : ''}`}>
        <div className="card">
          <h2>Ask a Question</h2>
          <form onSubmit={handleQuery}>
            <div className="form-group">
              <label htmlFor="question">Question</label>
              <textarea
                id="question"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="What would you like to know about your saved content?"
                required
              />
            </div>
            <button type="submit" className="button" disabled={queryLoading}>
              {queryLoading ? 'Thinking...' : 'Ask Question'}
            </button>
          </form>

          {answer && (
            <div className="answer-section">
              <h3 style={{ marginBottom: '12px', color: '#2c3e50' }}>Answer</h3>
              <div className="answer">{answer}</div>

              {sources.length > 0 && (
                <div className="sources">
                  <h3 style={{ marginBottom: '12px', color: '#2c3e50' }}>
                    Sources ({sources.length})
                  </h3>
                  {sources.map((source, idx) => (
                    <div key={idx} className="source">
                      <div className="source-header">
                        Source {idx + 1}
                        {source.source_url && (
                          <span style={{ marginLeft: '8px', fontSize: '12px' }}>
                            (
                            <a
                              href={source.source_url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="item-url"
                            >
                              {source.source_url}
                            </a>
                            )
                          </span>
                        )}
                      </div>
                      <div className="source-content">{source.content}</div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default App

