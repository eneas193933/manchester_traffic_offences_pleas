//= include moj.js
//= include modules/moj.FocusHandler.js
//= include modules/moj.PromptOnChange.js
//= include modules/moj.SelectionButtons.js

$(function() {
  jQuery.fx.off = true;

  $('[data-auto-refresh]').on('change', function() {
    window.location.href = $(this).val();
  });

  moj.init();
});
