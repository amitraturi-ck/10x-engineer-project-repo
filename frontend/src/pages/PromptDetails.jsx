import { useEffect, useState } from "react"
import { useParams, useNavigate } from "react-router-dom"
import { getPrompt, deletePrompt } from "../api/prompts"
import { getPromptVersions } from "../api/prompts"
import Modal from "../components/shared/Modal"
import LoadingSpinner from "../components/shared/LoadingSpinner"
export default function PromptDetails() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [prompt, setPrompt] = useState(null)
  const [versions, setVersions] = useState([])
  const [showModal, setShowModal] = useState(false)

  useEffect(() => {
    getPrompt(id).then(setPrompt)
  }, [id])

 if (!prompt) return <LoadingSpinner />
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

  return (
    <>
      <h2>{prompt.title}</h2>
      <p>{prompt.description}</p>
      <pre>{prompt.content}</pre>

      <button onClick={() => navigate(`/prompts/${id}/edit`)}>Edit</button>
      <button onClick={handleViewVersions}>Versions</button>
      <button onClick={handleDelete}>Delete</button>
      <Modal isOpen={showModal} onClose={() => setShowModal(false)}>
  <h3>Version History</h3>

  {versions.length === 0 && <p>No previous versions</p>}

  {versions.map(v => (
    <div key={v.version}>
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
    </>
  )
}
