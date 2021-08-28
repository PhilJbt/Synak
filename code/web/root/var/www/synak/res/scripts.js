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

function getPython(_scriptname){
  bFetching = true;
  $('.ui.modal').modal('show');
  $('#btn_proceed').addClass("loading");
  fetch('res/python/' + _scriptname + '.py')
    .then(function(response) {
      response.text().then(function(text) {
        $('#mdl_output').html(text);
        $('#btn_proceed').removeClass("loading");
      });
    });
}