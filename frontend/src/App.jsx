import { useState } from "react"
import "./App.css"
import axios from "axios"


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
     const response = await axios.post(
      "http://localhost:8000/generate-digest",
      { interests: interestList },
      { responseType: "stream" }
    )

    const reader = response.data.getReader()
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
    <div className="container">
      <h1>📰 Personalized News Digest</h1>
      <p className="subtitle">Enter your interests and get a fresh AI-generated news digest</p>

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
          {loading ? "Generating..." : "Generate"}
        </button>
      </div>

      {digest && (
        <div className="digest">
          <pre>{digest}</pre>
        </div>
      )}
    </div>
  )
}

export default App