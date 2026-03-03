import request from "./client.js"

export function getPrompts({ search = "", collectionId = "" } = {}) {
  const params = new URLSearchParams()

  if (search) params.append("search", search)
  if (collectionId) params.append("collection_id", collectionId)

  const query = params.toString() ? `?${params.toString()}` : ""
  return request(`/prompts${query}`)
}


export function getPrompt(id) {
  return request(`/prompts/${id}`)
}

export function createPrompt(data) {
  return request("/prompts", {
    method: "POST",
    body: JSON.stringify(data),
  })
}

export function updatePrompt(id, data) {
  return request(`/prompts/${id}`, {
    method: "PUT",
    body: JSON.stringify(data),
  })
}

export function deletePrompt(id) {
  return request(`/prompts/${id}`, {
    method: "DELETE",
  })
}
export function getPromptVersions(id) {
  return request(`/prompts/${id}/versions`)
}

export function runPrompt(id, variables = {}) {
  return request(`/prompts/${id}/run`, {
    method: "POST",
    body: JSON.stringify({ variables }),
  })
}
