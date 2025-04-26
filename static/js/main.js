let alerts = document.getElementsByClassName("alert");

setTimeout(() => {
  for (alert of alerts) {
    alert.remove();
  }
}, 3000);

document.addEventListener("DOMContentLoaded", function () {
  const navbar = document.getElementById("mainNav");

  window.addEventListener("scroll", function () {
    if (window.scrollY > 0) {
      navbar.classList.add("scrolled");
    } else {
      navbar.classList.remove("scrolled");
    }
  });
});
