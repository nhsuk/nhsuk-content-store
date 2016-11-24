$(function() {
  var $form = $('#page-edit-form');
  var initialData = $form.serialize();
  var $previewButton = $('.action-revision-preview');

  $previewButton.on('click', function(event) {
    var $target = $(event.target);
    var action = $target.data('action');
    var windowName = $target.data('windowname');

    if ($target.attr('data-preview-disabled') === 'true') {
      alert('Unsaved changed, please save the page before previewing it.');
      return;
    }

    if (action && windowName) {
      window.open($target.data('action'), $target.data('windowname'));
    } else {
      console.error('data-action and/or data-windowname is missing on preview button');
    }
  });

  $form.on('change', function(event) {
    var currentData = $form.serialize();
    var isNewPage = $form.attr('action').indexOf('/add/') !== -1;
    var isDisabled = isNewPage || currentData !== initialData;

    $.each($previewButton, function() {
      $(this).attr('data-preview-disabled', isDisabled);
    });
  });
});
