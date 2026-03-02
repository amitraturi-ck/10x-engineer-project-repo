import { useNavigate } from "react-router-dom"
import { createPrompt } from "../api/prompts"
import PromptForm from "../components/prompts/PromptForm"

export default function CreatePrompt() {
  const navigate = useNavigate()

  const handleSubmit = async (data) => {
    await createPrompt(data)
    navigate("/")
  }

  return (
    <>
      <h2>Create Prompt</h2>
      <PromptForm onSubmit={handleSubmit} />
    </>
  )
}
