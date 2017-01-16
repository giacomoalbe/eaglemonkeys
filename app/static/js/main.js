$(document).ready(function () {
  $('.fields').hide();
  var $title = $('.countdown');

  var count = 0;
  var startTime, endTime; 
  var countdownIntervalId = setInterval(countDown, 1000);

  function stopTimeAndSubmit() {
    endTime = new Date();
    var timeElapsed = (endTime - startTime) / 1000;

    $('input[name="time-elapsed"]').val(timeElapsed);
  }

  function countDown() {
    if (count == 3) {
      clearInterval(countdownIntervalId);
      $title.text("Type, monkey, type!");
      $('.fields').show(300, function() {

        startTime = new Date();
        $('#fieldsForm').submit(stopTimeAndSubmit);
        $('input').first().focus();

      });

      return;
    } 

    $title.text(3-count);
    count++;
  }
});
