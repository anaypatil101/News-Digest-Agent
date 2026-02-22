import { useState } from "react"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"
import "./App.css"

function App() {
  const [interests, setInterests] = useState("")
  const [digest, setDigest] = useState("")
  const [loading, setLoading] = useState(false)

  const generateDigest = async () => {
    if (!interests.trim()) return

    setLoading(true)
    setDigest("")

    const interestList = interests.split(",").map(i => i.trim()).filter(Boolean)

    try {
      const response = await fetch("http://localhost:8000/generate-digest", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ interests: interestList }),
      })

      const reader = response.body.getReader()
      const decoder = new TextDecoder()

      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        setDigest(prev => prev + decoder.decode(value))
      }
    } catch (error) {
      setDigest("Something went wrong. Make sure the backend is running.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-wrapper">
      {/* Ambient background glow */}
      <div className="bg-glow bg-glow-1" />
      <div className="bg-glow bg-glow-2" />

      <div className="container">
        <header className="header">
          <div className="logo-badge">📰</div>
          <h1>News Digest</h1>
          <p className="subtitle">
            AI agents that scour the web, cut through the noise, and hand you a clean personalized digest of today's most relevant news 
          </p>
        </header>

        <div className="input-card">
          <label className="input-label">Your Interests</label>
          <div className="input-row">
            <input
              type="text"
              placeholder="e.g. AI, cricket, Indian startups"
              value={interests}
              onChange={e => setInterests(e.target.value)}
              onKeyDown={e => e.key === "Enter" && generateDigest()}
              disabled={loading}
            />
            <button onClick={generateDigest} disabled={loading}>
              {loading ? (
                <span className="btn-loading">
                  <span className="spinner" />
                  Generating
                </span>
              ) : (
                <>
                  <span className="btn-icon">✦</span>
                  Generate
                </>
              )}
            </button>
          </div>
        </div>

        {loading && !digest && (
          <div className="loader-card">
            <div className="loader-header">
              <div className="pulse-dot" />
              <span>Researching & writing your digest…</span>
            </div>
            <div className="skeleton-lines">
              <div className="skeleton skeleton-title" />
              <div className="skeleton skeleton-text" />
              <div className="skeleton skeleton-text short" />
              <div className="skeleton skeleton-text" />
              <div className="skeleton skeleton-text shorter" />
            </div>
          </div>
        )}

        {digest && (
          <div className="digest-card">
            <div className="digest-content">
              <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                components={{
                  a: ({ href, children }) => (
                    <a href={href} target="_blank" rel="noopener noreferrer">
                      {children}
                    </a>
                  ),
                }}
              >
                {digest}
              </ReactMarkdown>
            </div>
            {loading && (
              <div className="stream-indicator">
                <span className="typing-dot" />
                <span className="typing-dot" />
                <span className="typing-dot" />
              </div>
            )}
          </div>
        )}
      </div>

      <footer className="footer">
        MADE WITH ❤️ BY ANAY PATIL
      </footer>
    </div>
  )
}

export default App