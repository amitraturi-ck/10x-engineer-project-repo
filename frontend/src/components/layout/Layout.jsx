import Header from "./Header"
import Sidebar from "./Sidebar"

export default function Layout({ children }) {
  return (
    <div className="layout-root">
      <Header />

      <div className="layout-body">
        <Sidebar />
       <main className="app-content">
  <div className="app-content-inner">
    {children}
  </div>
</main>
      </div>
    </div>
  )
}
