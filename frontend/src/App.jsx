import { Routes, Route } from "react-router-dom"
import Layout from "./components/layout/Layout"

import Dashboard from "./pages/Dashboard"
import PromptDetails from "./pages/PromptDetails"
import CreatePrompt from "./pages/CreatePrompt"
import EditPrompt from "./pages/EditPrompt"
import Collections from "./pages/Collections"
import { useEffect } from "react"
import request from "./api/client";
function App() {
  useEffect(() => {
    request("/health")
      .then(res => console.log("API Response:", res))
      .catch(err => console.error("ERROR:", err))
  }, [])
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/prompts/:id" element={<PromptDetails />} />
        <Route path="/create" element={<CreatePrompt />} />
        <Route path="/collections" element={<Collections />} />
        <Route path="/prompts/:id/edit" element={<EditPrompt />} />
      </Routes>
    </Layout>
  )

}
console.log("BASE URL:", import.meta.env.VITE_API_BASE_URL +"      test")
export default App
