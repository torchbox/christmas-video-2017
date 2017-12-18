document.addEventListener("DOMContentLoaded", function(event) {
  registerFormCallback();
  createSocialSharingButtons();
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

function createSocialSharingButtons() {
    var options = {
        shares: ["email", "twitter", "facebook", "googleplus", "linkedin", "pinterest", "whatsapp"],
        showCount: true,
    };
    if (window.shareURL) {
        options.url = window.shareURL;
    }
    $(".js-socials-container").jsSocials(options);
}
