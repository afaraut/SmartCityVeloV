//$('#formSearch').live('submit', function(event) { // catch the form's submit event
//$(document).on('submit', '#formSearch', function(){
//$('#formSearch').submit(function(evt){ 
  $('#formSearch').submit(function(event){
  event.preventDefault();
  console.log($(this));
  $('#imgWait').show(); // Show the loading image
  $('body').append('<div id="fade"></div>'); // Add the fade layer to bottom of the body tag.
  $('#fade').css({'filter' : 'alpha(opacity=80)'}).fadeIn(); // Fade in the fade layer 
  $.ajax({ // create an AJAX call...
      data: $('#formSearch').serialize(), // get the form data
      type: $('#formSearch').attr('method'), // GET or POST
      url: $('#formSearch').attr('action'), // the file to call
      success: function(response) { // on success..
          $('#reponse').html(response); // update the DIV
          $('#imgWait').hide(); // Hide the loading image
          $('#fade').css({'filter' : 'alpha(opacity=80)'}).fadeOut(); // Fade out the fade layer 
          $('body').remove('<div id="fade"></div>'); // Remove the fade layer to bottom of the body tag.
      }
  });
  return false;
});