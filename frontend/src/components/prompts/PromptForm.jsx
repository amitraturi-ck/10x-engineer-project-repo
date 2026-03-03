import { useEffect, useState } from "react"
import { getCollections } from "../../api/collections"

export default function PromptForm({ initialData = {}, onSubmit }) {
  const [form, setForm] = useState({
    title: initialData.title || "",
    description: initialData.description || "",
    content: initialData.content || "",
    collection_id: initialData.collection_id || ""
  })

  const [collections, setCollections] = useState([])
  const [errors, setErrors] = useState({})
  const [submitting, setSubmitting] = useState(false)

  // =============================
  // Load collections
  // =============================
  useEffect(() => {
    async function load() {
      const data = await getCollections()
      setCollections(data.collections)
    }
    load()
  }, [])

  // =============================
  // Validation
  // =============================
  const validate = () => {
    const e = {}

    if (!form.title.trim()) {
      e.title = "Title is required"
    }

    if (!form.content.trim()) {
      e.content = "Prompt content is required"
    } else if (form.content.length < 10) {
      e.content = "Prompt must be at least 10 characters"
    }

    if (form.description.length > 500) {
      e.description = "Description too long (max 500 chars)"
    }

    setErrors(e)
    return Object.keys(e).length === 0
  }

  // =============================
  // Handle Input Change
  // =============================
  const handleChange = (e) => {
    const { name, value } = e.target

    setForm(prev => ({ ...prev, [name]: value }))

    // Clear error as user types (good UX)
    setErrors(prev => ({ ...prev, [name]: undefined }))
  }

  // =============================
  // Submit
  // =============================
  const handleSubmit = async (e) => {
    e.preventDefault()

    if (!validate()) return

    try {
      setSubmitting(true)
      await onSubmit(form)
    } finally {
      setSubmitting(false)
    }
  }

  // =============================
  // UI
  // =============================
  return (
    <form onSubmit={handleSubmit} className="space-y-4 max-w-xl">

      {/* Title */}
      <div>
        <input
          name="title"
          value={form.title}
          onChange={handleChange}
          placeholder="Title"
          className="w-full"
        />
        {errors.title && (
          <p className="text-red-400 text-sm mt-1">{errors.title}</p>
        )}
      </div>

      {/* Description */}
      <div>
        <input
          name="description"
          value={form.description}
          onChange={handleChange}
          placeholder="Description (optional)"
          className="w-full"
        />
        {errors.description && (
          <p className="text-red-400 text-sm mt-1">{errors.description}</p>
        )}
      </div>

      {/* Content */}
      <div>
        <textarea
          name="content"
          value={form.content}
          onChange={handleChange}
          rows={8}
          placeholder="Write your prompt..."
          className="w-full"
        />
        {errors.content && (
          <p className="text-red-400 text-sm mt-1">{errors.content}</p>
        )}
      </div>

      {/* Collection */}
      <div>
        <select
          name="collection_id"
          value={form.collection_id || ""}
          onChange={handleChange}
          className="w-full"
        >
          <option value="">No Collection</option>
          {collections.map(c => (
            <option key={c.id} value={c.id}>
              {c.name}
            </option>
          ))}
        </select>
      </div>

      {/* Submit */}

      <button
        type="submit"
        disabled={submitting}
      >
        {submitting ? "Saving..." : "Save Prompt"}
      </button>
    </form>
  )
}
