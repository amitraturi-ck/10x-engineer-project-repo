import { useState } from 'react'

export default function CollectionForm({ onSubmit }) {
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')

  const handleSubmit = e => {
    e.preventDefault()
    onSubmit({ name, description })
  }

  return (
    <form onSubmit={handleSubmit} className="form">
      <input value={name} onChange={e => setName(e.target.value)} placeholder="Collection Name" required />
      <input value={description} onChange={e => setDescription(e.target.value)} placeholder="Description" />
      <button type="submit">Create</button>
    </form>
  )
}
