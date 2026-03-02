import { useNavigate } from "react-router-dom"

export default function Header() {
  const navigate = useNavigate()

  return (
    <header className="header">
      <div className="logo" onClick={() => navigate("/")}>
        PromptLab
        <span>AI Prompt Engineering Platform</span>
      </div>

      <nav>
        <button onClick={() => navigate("/")}>All Prompts</button>
        <button onClick={() => navigate("/collections")}>
          Manage Collections
        </button>
        <button onClick={() => navigate("/create")}>
          Create Prompt
        </button>
      </nav>
    </header>
  )
}
