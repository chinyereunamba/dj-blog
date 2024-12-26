// Get the current theme preference from the system
const systemTheme = window.matchMedia("(prefers-color-scheme: dark)").matches;

// Apply the correct theme based on the system preference
if (systemTheme) {
  document.documentElement.setAttribute('data-theme', 'dark');
} else {
  document.documentElement.setAttribute('data-theme', 'light');
}

// Allow users to toggle the theme manually
const toggleButton = document.getElementById('theme-toggle');
toggleButton.addEventListener('click', () => {
  const currentTheme = document.documentElement.getAttribute('data-theme');
  const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', newTheme);
});
