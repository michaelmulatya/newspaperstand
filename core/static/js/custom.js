
function submit_message(message) {
        $.post( "/send_message", {message: message}, handle_response);

    }

$('#target').on('submit', function(e){
        e.preventDefault();
        const input_message = $('#input_message').val()
        submit_message(input_message)
});



<!--/.Carousel Wrapper-->

$('.carousel.carousel-multi-item.v-2 .carousel-item').each(function(){
  var next = $(this).next();
  if (!next.length) {
    next = $(this).siblings(':first');
  }
  next.children(':first-child').clone().appendTo($(this));

  for (var i=0;i<3;i++) {
    next=next.next();
    if (!next.length) {
      next = $(this).siblings(':first');
    }
    next.children(':first-child').clone().appendTo($(this));
  }
});


$('#myModal').on('shown.bs.modal', function () {
  $('#myInput').trigger('focus')
})

