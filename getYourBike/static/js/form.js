//$('#formSearch').live('submit', function(event) { // catch the form's submit event
//$(document).on('submit', '#formSearch', function(){
//$('#formSearch').submit(function(evt){ 
$(document).ready(function() {
  $('#formSearch').submit(function(event){
    alert("test");
    event.preventDefault();
    console.log($(this));
    $('#imgWait').show(); // Show the loading image
    $('body').append('<div id="fade"></div>'); // Add the fade layer to bottom of the body tag.
    $('#fade').css({'filter' : 'alpha(opacity=80)'}).fadeIn(); // Fade in the fade layer 

    var csrftoken = $( "input[name$='csrfmiddlewaretoken']" ).val(); // Get the token
    var day_month = $("#id_day_month").val();
    var day_day = $("#id_day_day").val();
    var day_year = $("#id_day_year").val();
    var hour_hour = $("#id_hour_hour").val();
    var hour_minute = $("#id_hour_minute").val();
    var station = $("#id_station").val();

    $.ajax({ // create an AJAX call...
        data: {"day_month":day_month, "day_day" : day_day, "day_year" : day_year, "hour_hour" : hour_hour, "hour_minute" : hour_minute, "station" : station, "csrfmiddlewaretoken" : csrftoken}, // get the form data
        type: $(this).attr('method'), // GET or POST
        url: $(this).attr('action'), // the file to call
        success: function(response) { // on success..
            $('#reponse').html(response); // update the DIV
            $('#imgWait').hide(); // Hide the loading image
            $('#fade').css({'filter' : 'alpha(opacity=80)'}).fadeOut(); // Fade out the fade layer 
            $('body').remove('<div id="fade"></div>'); // Remove the fade layer to bottom of the body tag.
        }
    });
    return false;
  });
});