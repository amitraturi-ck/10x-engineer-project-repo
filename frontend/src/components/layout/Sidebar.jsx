import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import { getCollections } from "../../api/collections"
import { useSearchParams } from "react-router-dom"

export default function Sidebar() {
  const [collections, setCollections] = useState([])
  const navigate = useNavigate()
const [params] = useSearchParams()
  useEffect(() => {
    getCollections().then(data => setCollections(data.collections))
  }, [])

  return (
    <aside className="sidebar">
      <h4 className="sidebar-title">Collections</h4>

      {collections.length === 0 && (
        <p className="empty">No collections yet</p>
      )}

      {collections.map(c => (
        <button
  key={c.id}
  className={`collection-item ${params.get("collection") === c.id ? "active" : ""}`}
  onClick={() => navigate(`/?collection=${c.id}`)}
>
          {c.name}
        </button>
      ))}
    </aside>
  )
}
