import PromptCard from "./PromptCard"

export default function PromptList({
  prompts,
  onSelect,
  onDelete,
  onViewVersions,
  onEdit
}) {
  if (!prompts.length) {
    return (
      <div className="empty-state">
        <h3>No prompts yet</h3>
        <p>Create your first AI prompt to get started.</p>
      </div>
    )
  }

  return (
    <div className="prompt-grid">
      {prompts.map(p => (
        <PromptCard
          key={p.id}
          prompt={p}
          onClick={onSelect}
          onDelete={onDelete}
          onViewVersions={onViewVersions}
          onEdit={onEdit}
        />
      ))}
    </div>
  )
}
