// Create cosmic loader
function showCosmicLoader(message = "Warping into the cosmos...") {
  const overlay = document.createElement("div");
  overlay.classList.add("cosmic-loader");

  overlay.innerHTML = `
    <div class="spinner"></div>
    <p>${message}</p>
  `;

  document.body.appendChild(overlay);
}

// Hide cosmic loader
function hideCosmicLoader() {
  const overlay = document.querySelector(".cosmic-loader");
  if (overlay) overlay.remove();
}

// Show loader on form submit
document.addEventListener("DOMContentLoaded", () => {
  const forms = document.querySelectorAll("form");
  forms.forEach((form) => {
    form.addEventListener("submit", () => {
      showCosmicLoader();
    });
  });
});
