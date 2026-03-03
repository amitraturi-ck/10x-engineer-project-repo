import { useState } from 'react'

export default function CollectionForm({ onSubmit }) {
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')

  const handleSubmit = e => {
    e.preventDefault()
    onSubmit({ name, description })
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6 max-w-xl">

      <div>
        <input
          value={name}
          onChange={e => setName(e.target.value)}
          placeholder="Enter collection name"
          required
        />
      </div>

      <div>
        <label className="block text-sm mb-2">
          Description
        </label>
        <input
          value={description}
          onChange={e => setDescription(e.target.value)}
          placeholder="Optional description"
        />
      </div>

      <div style={{ display: "flex", justifyContent: "flex-end" }}>
        <button type="submit">
          Create Collection
        </button>
      </div>

    </form>
  )
}
