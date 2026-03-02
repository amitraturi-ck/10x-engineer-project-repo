export default function PromptCard({
  prompt,
  onClick,
  onDelete,
  onViewVersions,
  onEdit
}) {
  return (
    <div className="bg-[#1e293b] border border-gray-700 rounded-xl p-6 shadow-md hover:shadow-lg transition">

      <h3
        onClick={() => onClick(prompt.id)}
        className="text-lg font-semibold cursor-pointer hover:text-indigo-400"
      >
        {prompt.title}
      </h3>

      <p className="text-gray-400 mt-2 text-sm">
        {prompt.description || "No description provided"}
      </p>

      <p className="text-xs text-gray-500 mt-2">
        Updated: {new Date(prompt.updated_at).toLocaleString()}
      </p>

     <div className="card-actions">
  <button onClick={() => onEdit(prompt.id)}>Edit</button>
  <button onClick={() => onViewVersions(prompt.id)}>Versions</button>
  <button className="danger" onClick={() => onDelete(prompt.id)}>Delete</button>
</div>
    </div>
  )
}
