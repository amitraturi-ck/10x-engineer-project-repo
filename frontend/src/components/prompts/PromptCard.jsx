export default function PromptCard({
  prompt,
  onClick,
  onDelete,
  onViewVersions,
  onEdit
}) {
  return (
    <div className="card">

      <h3
        onClick={() => onClick(prompt.id)}
        className="cursor-pointer"
      >
        {prompt.title}
      </h3>

      <p className="text-muted">
        {prompt.description || "No description provided"}
      </p>

      <p className="text-xs text-muted mt-2">
        Updated: {new Date(prompt.updated_at).toLocaleString()}
      </p>

      <div className="card-actions">
        <button onClick={() => onEdit(prompt.id)}>Edit</button>
        <button onClick={() => onViewVersions(prompt.id)}>Versions</button>
        <button
          className="danger"
          onClick={() => onDelete(prompt.id)}
        >
          Delete
        </button>
      </div>

    </div>
  )
}
