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
      buttons[i].classList.add('is-loading');
    }
    var fields = target.querySelectorAll('input');
    for (var i = 0; i < fields.length; i++) {
        fields[i].readonly = true;
    }
    $('.hide-if-generating-video').fadeOut({
        complete: function() {
            $('.show-if-generating-video').fadeIn({
                complete: function() {
                },
            });
        },
    });
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
    var $jsSocialsContainer = $(".js-socials-container");
    if ($jsSocialsContainer.length) {
        $jsSocialsContainer.jsSocials(options);
    }
}
