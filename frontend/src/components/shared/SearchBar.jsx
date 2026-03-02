export default function SearchBar({ onChange }) {
  return (
    <input
      type="text"
      placeholder="Search prompts..."
      onChange={(e) => onChange(e.target.value)}
      className="search-input"
    />
  )
}
