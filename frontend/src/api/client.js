const BASE_URL = import.meta.env.VITE_API_BASE_URL

async function request(endpoint, options = {}) {
  const response = await fetch(`${BASE_URL}${endpoint}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  })

  if (!response.ok) {
    let message = "Request failed"
    try {
      const data = await response.json()
      message = data.detail || message
    } catch (_) {print(_)}
    throw new Error(message)
  }

  if (response.status === 204) return null

  return response.json()
}

export default request
