import { useEffect, useState } from "react"
import { useParams, useNavigate } from "react-router-dom"

import {
  getPrompt,
  deletePrompt,
  getPromptVersions,
  runPrompt
} from "../api/prompts"

import Modal from "../components/shared/Modal"
import LoadingSpinner from "../components/shared/LoadingSpinner"

export default function PromptDetails() {
  const { id } = useParams()
  const navigate = useNavigate()

  const [prompt, setPrompt] = useState(null)
  const [versions, setVersions] = useState([])
  const [showModal, setShowModal] = useState(false)

  // Execution state
  const [messages, setMessages] = useState([])
  const [running, setRunning] = useState(false)
  const [runError, setRunError] = useState(null)

  // =============================
  // Load prompt
  // =============================
  useEffect(() => {
    getPrompt(id).then(setPrompt)
  }, [id])

  if (!prompt) return <LoadingSpinner />

  // =============================
  // Handlers
  // =============================
  const handleViewVersions = async () => {
    const data = await getPromptVersions(id)
    setVersions(data.versions)
    setShowModal(true)
  }

  const handleDelete = async () => {
    if (!window.confirm("Delete this prompt?")) return
    await deletePrompt(id)
    navigate("/")
  }

  const handleRun = async () => {
    try {
      setRunError(null)
      setRunning(true)

      // Add user message (prompt content)
      const userMessage = {
        role: "user",
        content: prompt.content
      }

      setMessages(prev => [...prev, userMessage])

      const response = await runPrompt(id, {})

      const aiMessage = {
        role: "assistant",
        content: response.result
      }

      setMessages(prev => [...prev, aiMessage])

    } catch (err) {
      setRunError(err.message)
    } finally {
      setRunning(false)
    }
  }

  // =============================
  // UI
  // =============================
  return (
    <div className="execution-layout">

      {/* ================= LEFT SIDE ================= */}
      <div className="execution-left">

        <div className="card">

          <h2>{prompt.title}</h2>

          <p className="text-muted">
            {prompt.description || "No description provided"}
          </p>

          <pre className="prompt-content">
            {prompt.content}
          </pre>

          <div className="card-actions">

            <button onClick={() => navigate(`/prompts/${id}/edit`)}>
              Edit
            </button>

            <button onClick={handleViewVersions}>
              Versions
            </button>

            <button className="danger" onClick={handleDelete}>
              Delete
            </button>

            <button
              className="run-btn"
              onClick={handleRun}
              disabled={running}
            >
              {running ? "Running..." : "Run"}
            </button>

          </div>
        </div>

      </div>

      {/* ================= RIGHT SIDE ================= */}
      <div className="execution-right">

        <h3>Execution Panel</h3>

        {runError && (
          <div className="error-box">
            {runError}
          </div>
        )}

        {messages.length === 0 && (
          <div className="empty-state">
            Click "Run" to execute this prompt.
          </div>
        )}

        <div className="chat-container">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`chat-message ${msg.role}`}
            >
              {msg.content}
            </div>
          ))}
        </div>

      </div>

      {/* ================= MODAL ================= */}
      <Modal isOpen={showModal} onClose={() => setShowModal(false)}>
        <h3>Version History</h3>

        {versions.length === 0 && <p>No previous versions</p>}

        {versions.map(v => (
          <div key={v.version} className="version-block">
            <strong>Version {v.version}</strong>

            <div>
              <small>
                Archived at: {new Date(v.archived_at).toLocaleString()}
              </small>
            </div>

            <pre>{v.content}</pre>
            <hr />
          </div>
        ))}
      </Modal>

    </div>
  )
}
