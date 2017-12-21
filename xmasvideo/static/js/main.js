document.addEventListener("DOMContentLoaded", function(event) {
  registerFormCallback();
});

function registerFormCallback() {
  form = document.querySelector('#postcard-create-form');
  if (form) {
      form.addEventListener('submit', formSubmitCallback);
      var messageInput = form.querySelector('input[name="message"]');
      if (messageInput) {
          messageInput.addEventListener('keyup', messageKeyDownCallback);
      }
  }
}

function messageKeyDownCallback(event) {
    var target = event.target;
    var regex = /^[a-zA-Z ]+$/;
    if (regex.test(target.value) !== true)
        target.value = target.value.replace(/[^a-zA-Z ]+/, '');
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
