$('#formSearch').live('submit', function(event) { // catch the form's submit event
  event.preventDefault();
  $.ajax({ // create an AJAX call...
      data: $(this).serialize(), // get the form data
      type: $(this).attr('method'), // GET or POST
      url: $(this).attr('action'), // the file to call
      success: function(response) { // on success..
          $('#reponse').html(response); // update the DIV
      }
  });
  return false;
});