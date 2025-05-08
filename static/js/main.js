// Remove alerts after 3 seconds
let alerts = document.getElementsByClassName("alert");

setTimeout(() => {
  for (alert of alerts) {
    alert.remove();
  }
}, 3000);

// Add dynamic scrolled class for header styles
document.addEventListener("DOMContentLoaded", function () {
  const navbar = document.getElementById("mainNav");
  const isHomePage = window.location.pathname === "/";

  if (isHomePage) {
    window.addEventListener("scroll", function () {
      if (window.scrollY > 0) {
        navbar.classList.add("scrolled");
      } else {
        navbar.classList.remove("scrolled");
      }
    });
  } else {
    navbar.classList.add("scrolled");
  }
});
