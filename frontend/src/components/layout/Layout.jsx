import Header from './Header';
import Sidebar from './Sidebar';
import { Outlet } from 'react-router-dom'; // Using Outlet to match App.jsx routing setup

export default function Layout({ children }) {
  return (
    <div className="layout-root dark:bg-gray-950 dark:text-gray-100 transition-colors duration-200">
      <Header />
      <div className="layout-body">
        <Sidebar />
        <main className="app-content dark:bg-gray-900 transition-colors duration-200">
          <div className="app-content-inner">
            {children || <Outlet />}
          </div>
        </main>
      </div>
    </div>
  );
}
