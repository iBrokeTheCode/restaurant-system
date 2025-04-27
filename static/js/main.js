let alerts = document.getElementsByClassName("alert");

setTimeout(() => {
  for (alert of alerts) {
    alert.remove();
  }
}, 3000);
