export default function LoadingSpinner({ label = "Loading..." }) {
  return (
    <div className="flex items-center justify-center py-10">
      <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-brand mr-3" />
      <span className="text-gray-400">{label}</span>
    </div>
  )
}
