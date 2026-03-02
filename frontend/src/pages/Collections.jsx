import { useEffect, useState } from "react"
import {
  getCollections,
  createCollection,
  deleteCollection,
} from "../api/collections"
import CollectionList from "../components/collections/CollectionList"
import CollectionForm from "../components/collections/CollectionForm"

export default function Collections() {
  const [collections, setCollections] = useState([])

  // ✅ effect contains async instead of calling external loader
  useEffect(() => {
    let mounted = true

    async function fetchCollections() {
      const data = await getCollections()
      if (mounted) setCollections(data.collections)
    }

    fetchCollections()
    return () => { mounted = false }
  }, [])

  const handleCreate = async (data) => {
    await createCollection(data)
    const refreshed = await getCollections()
    setCollections(refreshed.collections)
  }

  const handleDelete = async (id) => {
    await deleteCollection(id)
    const refreshed = await getCollections()
    setCollections(refreshed.collections)
  }

  return (
    <>
      <h2>Collections</h2>
      <CollectionForm onSubmit={handleCreate} />
      <CollectionList collections={collections} onDelete={handleDelete} />
    </>
  )
}
