export default function CollectionList({ collections, onDelete }) {
  if (!collections?.length) return <p>No collections yet.</p>

  return (
    <ul>
      {collections.map(c => (
        <li key={c.id}>
          {c.name}
          {onDelete && (
            <button
              onClick={() => onDelete(c.id)}
              style={{ marginLeft: 10 }}
            >
              Delete
            </button>
          )}
        </li>
      ))}
    </ul>
  )
}
