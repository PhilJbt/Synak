$('.ui.dropdown').dropdown();

var bFetching = false;

function showModal(_type) {
  bFetching = true;
  $('#mdl_output').addClass("loading");
  fetch('res/template/' + _type + '.tpl')
    .then(function(response) {
      response.text().then(function(text) {
        $('.ui.modal').html(text);
        $('.ui.modal').modal('show');
        $('#mdl_output').removeClass("loading");
        bFetching = false;
      });
    });
}

function getPython(_scriptname){
  bFetching = true;
  $('.ui.modal').modal('show');
  $('#btn_proceed').addClass("loading");
  $('#mdl_output').addClass("loading");
  fetch('res/python/' + _scriptname + '.py')
    .then(function(response) {
      response.text().then(function(text) {
        $('#mdl_output').html(text);
        $('#btn_proceed').removeClass("loading");
        $('#mdl_output').removeClass("loading");

        $('.message .close').on('click', function() {
          $(this).closest('.message').transition('fade');
        });
      });
    });
}