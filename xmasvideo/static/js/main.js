document.addEventListener("DOMContentLoaded", function(event) {
  registerFormCallback();
});

function registerFormCallback() {
  form = document.querySelector('#postcard-create-form');
  if (form) {
      form.addEventListener('submit', formSubmitCallback);
  }
}

function formSubmitCallback(event) {
  var target = event.target;
  var buttons = target.querySelectorAll('button');
  for (var i = 0; i < buttons.length; i++) {
      buttons[i].disabled = true;
  }
  document.querySelector('#loading-label').style.display = 'block';
  target.submit();
}
