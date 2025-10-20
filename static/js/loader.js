document.addEventListener("DOMContentLoaded", () => {
  const forms = document.querySelectorAll("form");

  forms.forEach((form) => {
    form.addEventListener("submit", () => {
      const overlay = document.createElement("div");
      overlay.classList.add("cosmic-loader");
      overlay.innerHTML = `
        <div class="spinner"></div>
        <p>Warping into the cosmos...</p>
      `;
      document.body.appendChild(overlay);
    });
  });
});
