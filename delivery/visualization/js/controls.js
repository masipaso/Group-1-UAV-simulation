/**
*	UI Controls
*/
$( document ).ready(function() {
  // Reset
  $("#controls-reset").click(function() {
    $("#controls-reset").prop("disabled", true);
    reset();
  });
  // Play
  $("#controls-play").click(function() {
    $("#controls-play").prop("disabled", true);
    $("#controls-pause").prop("disabled", false);
    $("#controls-step").prop("disabled", true);
    run();
  });
  // Step
  $("#controls-step").click(function() {
    step();
  });
  // Pause
  $("#controls-pause").click(function() {
    $("#controls-pause").prop("disabled", true);
    $("#controls-play").prop("disabled", false);
    $("#controls-step").prop("disabled", false);
    $("#controls-reset").prop("disabled", false);
    pause();
  });
  // FPS
  $("#controls-fps").change(function() {
    changeFPS($(this).val());
  });

  /**
  * Mouse events
  */
  function getMousePosition(canvas, event) {
    const rect = canvas.getBoundingClientRect();
    return {
      x: event.clientX - rect.left,
      y: event.clientY - rect.top
    };
  };

  const realWorld = $(".real-world")[0];
  realWorld.addEventListener('mousemove', function(event) {
    var mousePosition = getMousePosition(realWorld, event);
    $("#mouse-position").html("x: " + mousePosition.x + ", y: " + mousePosition.y);
  });
});
