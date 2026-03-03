import { useTheme } from "../../context/ThemeContext";

export default function ThemeToggle() {
  const { isDark, toggleTheme } = useTheme();

  return (
    <button
      onClick={toggleTheme}
      className="theme-toggle"
      aria-label="Toggle theme"
    >
      <div className={`toggle-track ${isDark ? "active" : ""}`}>
        <div className="toggle-thumb" />
      </div>
    </button>
  );
}
