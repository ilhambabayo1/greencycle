// GreenCycle UI enhancements

// Confirm before deleting an item
document.querySelectorAll(".inline-form button").forEach((btn) => {
  btn.addEventListener("click", (e) => {
    if (!confirm("Delete this item?")) e.preventDefault();
  });
});

// Show a toast notification (used after form actions)
function showToast(message) {
  const toast = document.createElement("div");
  toast.className = "toast";
  toast.textContent = message;
  document.body.appendChild(toast);
  requestAnimationFrame(() => toast.classList.add("show"));
  setTimeout(() => {
    toast.classList.remove("show");
    setTimeout(() => toast.remove(), 300);
  }, 2500);
}

// Welcome toast on load
window.addEventListener("DOMContentLoaded", () => {
  if (window.location.pathname === "/") showToast("Welcome to GreenCycle!");
});
