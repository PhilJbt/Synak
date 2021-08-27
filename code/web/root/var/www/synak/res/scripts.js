$('.ui.dropdown').dropdown();

var bFetching = false;

function showModal(_type) {
  bFetching = true;
  $('#loader').addClass("active");
  fetch('res/template/' + _type + '.tpl')
    .then(function(response) {
      response.text().then(function(text) {
        $('.ui.modal').html(text);
        $('.ui.modal').modal('show');
        $('#loader').removeClass("active");
        bFetching = false;
      });
    });
}

function getPython(){
  bFetching = true;
  $('.ui.modal').modal('show');
  $('#loader').addClass("active");
  fetch('res/python/test.py')
    .then(function(response) {
      response.text().then(function(text) {
        console.log(text);
        $('#loader').removeClass("active");
      });
    });
}