export default function ErrorMessage({ message, retry }) {
  return (
    <div className="bg-red-500/10 border border-red-500 text-red-300 p-4 rounded">
      <p className="mb-2">{message}</p>
      {retry && (
        <button onClick={retry} className="text-sm underline">
          Try again
        </button>
      )}
    </div>
  )
}
