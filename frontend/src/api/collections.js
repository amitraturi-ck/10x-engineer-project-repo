import request from "./client.js"

export function getCollections() {
  return request("/collections")
}

export function createCollection(data) {
  return request("/collections", {
    method: "POST",
    body: JSON.stringify(data),
  })
}

export function deleteCollection(id) {
  return request(`/collections/${id}`, {
    method: "DELETE",
  })
}
