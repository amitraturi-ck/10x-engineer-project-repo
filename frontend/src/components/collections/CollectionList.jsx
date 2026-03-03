export default function CollectionList({ collections, onDelete }) {
  if (!collections?.length) {
    return <p className="empty-state">No collections yet</p>
  }

  return (
    <div>
      {collections.map(c => (
        <div key={c.id} className="collection-item-wrapper">
          <button className="collection-item">
            {c.name}
          </button>

          {onDelete && (
            <button
              className="danger small-btn"
              onClick={() => onDelete(c.id)}
            >
              Delete
            </button>
          )}
        </div>
      ))}
    </div>
  )
}
