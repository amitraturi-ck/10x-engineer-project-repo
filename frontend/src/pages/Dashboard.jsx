import { useEffect, useState } from "react"
import { useNavigate, useSearchParams } from "react-router-dom"

import { getPrompts, deletePrompt } from "../api/prompts"
import { getCollections } from "../api/collections"

import PromptList from "../components/prompts/PromptList"
import SearchBar from "../components/shared/SearchBar"
import LoadingSpinner from "../components/shared/LoadingSpinner"
import { getPromptVersions } from "../api/prompts"
import Modal from "../components/shared/Modal"

export default function Dashboard() {
  const [prompts, setPrompts] = useState([])
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()
  const [params] = useSearchParams()
  const collectionId = params.get("collection") || ""
  const [collectionName, setCollectionName] = useState("")
  const [versions, setVersions] = useState([])
  const [showModal, setShowModal] = useState(false)
  const [setSelectedPromptId] = useState(null)
  const handleEdit = (id) => navigate(`/prompts/${id}/edit`)
  const [error, setError] = useState(null)

  // ✅ Effect now owns the async logic (no external setState call)
  useEffect(() => {
    let mounted = true

    async function fetchData() {
      try {
        setError(null)
        setLoading(true)

        const data = await getPrompts({ collectionId })

        if (!mounted) return

        setPrompts(data.prompts)
      } catch {
        setError("Unable to load prompts. Please check your connection.")
      } finally {
        setLoading(false)
      }
    }

    fetchData()
    return () => { mounted = false }
  }, [collectionId])

  const handleViewVersions = async (id) => {
    const data = await getPromptVersions(id)
    setVersions(data.versions)
    setSelectedPromptId(id)
    setShowModal(true)
  }

  const handleSearch = async (value) => {
    const data = await getPrompts({ search: value, collectionId })
    setPrompts(data.prompts)
  }

  const handleDelete = async (id) => {
    if (!window.confirm("Delete this prompt?")) return

    await deletePrompt(id)

    // reload using SAME filters
    const data = await getPrompts({ collectionId })
    setPrompts(data.prompts)
  }

  const handleSelect = (id) => navigate(`/prompts/${id}`)

  if (loading) return <LoadingSpinner />

  return (
    <div className="page">

      <div className="page-header">
        <h2>All Prompts</h2>
        <SearchBar onChange={handleSearch} />
      </div>

      {collectionId && (
        <p className="filter-label">
          Filtering by: <strong>{collectionName}</strong>
        </p>
      )}

      {error && (
        <div className="error-box">
          <span>{error}</span>
          <button className="close-error" onClick={() => setError(null)}>&times;</button>
        </div>
      )}

      {/* ✅ THIS wrapper was missing */}
      <div className="grid">
        <PromptList
          prompts={prompts}
          onSelect={handleSelect}
          onDelete={handleDelete}
          onViewVersions={handleViewVersions}
          onEdit={handleEdit}
        />
      </div>
      <Modal isOpen={showModal} onClose={() => setShowModal(false)}>
        <h3>Version History</h3>

        {versions.length === 0 && <p>No previous versions</p>}

        {versions.map(v => (
          <div key={v.version} style={{ marginBottom: 15 }}>
            <strong>Version {v.version}</strong>

            <div>
              <small>
                Archived at: {new Date(v.archived_at).toLocaleString()}
              </small>
            </div>

            <pre style={{ background: "#f5f5f5", padding: 10 }}>
              {v.content}
            </pre>

            <hr />
          </div>
        ))}

        <button onClick={() => setShowModal(false)}>Close</button>
      </Modal>
    </div>
  )
}
