import { useNavigate } from 'react-router-dom';
import ThemeToggle from '../shared/ThemeToggle'; // Adjust path based on where you saved it

export default function Header() {
  const navigate = useNavigate();

  return (
    <header className="header dark:bg-gray-900 dark:border-gray-800 transition-colors duration-200">
      <div className="logo" onClick={() => navigate('/')}>
        PromptLab
        <span>AI Prompt Engineering Platform</span>
      </div>

      <nav className="flex items-center space-x-4">
        <button
          onClick={() => navigate('/')}
          className="dark:text-gray-200 dark:hover:text-white"
        >
          All Prompts
        </button>
        <button
          onClick={() => navigate('/collections')}
          className="dark:text-gray-200 dark:hover:text-white"
        >
          Manage Collections
        </button>
        <button
          onClick={() => navigate('/create')}
          className="dark:text-gray-200 dark:hover:text-white"
        >
          Create Prompt
        </button>

        {/* Added the ThemeToggle right after the navigation buttons */}
        <div className="pl-4 border-l border-gray-200 dark:border-gray-700">
          <ThemeToggle />
        </div>
      </nav>
    </header>
  );
}
