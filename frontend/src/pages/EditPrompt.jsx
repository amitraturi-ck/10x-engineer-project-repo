import { useEffect, useState } from "react"
import { useNavigate, useParams } from "react-router-dom"
import { getPrompt, updatePrompt } from "../api/prompts"
import PromptForm from "../components/prompts/PromptForm"
import LoadingSpinner from "../components/shared/LoadingSpinner"

export default function EditPrompt() {
  const { id } = useParams()
  const navigate = useNavigate()

  const [prompt, setPrompt] = useState(null)

  useEffect(() => {
    async function load() {
      const data = await getPrompt(id)
      setPrompt(data)
    }
    load()
  }, [id])

  const handleSubmit = async (data) => {
    await updatePrompt(id, data)
    navigate("/") // go back to dashboard
  }

  if (!prompt) return <LoadingSpinner />

  return (
    <>
      <h2>Edit Prompt</h2>
      <PromptForm initialData={prompt} onSubmit={handleSubmit} />
    </>
  )
}
