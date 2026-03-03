import { useEffect, useState } from "react";
import { useNavigate, useSearchParams, useLocation } from "react-router-dom";
import { getCollections } from "../../api/collections";

export default function Sidebar() {
  const [collections, setCollections] = useState([]);
  const navigate = useNavigate();
  const [params] = useSearchParams();
  const location = useLocation();

  useEffect(() => {
    async function load() {
      try {
        const data = await getCollections();
        setCollections(data.collections);
      } catch {
        setCollections([]);
      }
    }

    load();
  }, [location]); // refresh when route changes

  return (
    <aside className="sidebar">
      <h4 className="sidebar-title">Collections</h4>

      {collections.length === 0 && (
        <p className="empty-state">No collections yet</p>
      )}

      {collections.map((c) => (
        <button
          key={c.id}
          className={`sidebar-collection ${
            params.get("collection") === String(c.id) ? "active" : ""
          }`}
          onClick={() => navigate(`/?collection=${c.id}`)}
        >
          {c.name}
        </button>
      ))}
    </aside>
  );
}
