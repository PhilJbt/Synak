$('.ui.dropdown').dropdown();
$('#popup_signin').popup({
inline   : false,
hoverable: true,
position : 'bottom left',
on : 'click',
delay: {
  show: 0,
  hide: 500
 }
});
$('#popup_info').popup();

var bFetching = false;

function enableMessageClose() {
  $('.message .close').on('click', function() {
    $(this).closest('.message').transition('fade');
  });
}

function errorMessage(_error) {
  $('#mdl_output').html(
    '<div class="ui icon message '
    + _error["colr"] + '"><i class="close icon"></i><i class="'
    + _error["icon"] + ' icon"></i><div class="content"><div class="header">'
    + _error["titl"] + '</div><p>'
    + _error["mess"] + '</p></div></div>'
  );
  $('#mdl_output').removeClass("loading");

  enableMessageClose();
}

function prepReq_init() {
  $('#mdl_output').addClass("loading");
}

function prepReq_uninit(_text) {
  $('.ui.modal').html(_text);
  $('.ui.modal').modal('show');
  $('#mdl_output').removeClass("loading");
  enableMessageClose();
}

function procReq_init() {
  $('#btn_proceed').addClass("loading");
  $('#btn_proceed').addClass("disabled");
  $('#mdl_output').addClass("loading");
}

function procReq_uninit(_text) {
  $('#mdl_output').html(_text);
  $('#btn_proceed').removeClass("loading");
  $('#btn_proceed').removeClass("disabled");
  $('#mdl_output').removeClass("loading");
  $('.ui.modal').modal('hide');
  enableMessageClose();
}

function req_uninit() {
  $('#btn_proceed').removeClass("loading");
  $('#btn_proceed').removeClass("disabled");
  $('#mdl_output').removeClass("loading");
  $('.ui.modal').modal('hide');
}

async function sendReq(_scriptname, _action, _file) {
  $('#mdl_output').html("");

  try {
    const config = {
      method: 'POST',
      headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({
      'type': _action,
      'data': 'mydata',
      'file' : _file
      })
    }
    const response = await fetch('res/python/' + _scriptname + '.py', config);
    if (response.ok
      && response.status == 200) {
      var res = await response.json();
      console.log(res["type"]);
      console.log(res["data"]);
      if (res["type"] == "prep")
        prepReq_uninit(res["data"]);
      else if (res["type"] == "proc")
        procReq_uninit(res["data"]);
      else if (res["type"] == "erro") {
        errorMessage(JSON.parse(res["data"]));
        req_uninit();
      }
    } else {
      data = {
        "colr": "red",
        "icon": "exclamation",
        "titl": "WEB PANEL ERROR",
        "mess": "unknown error"
      }
      errorMessage(data);
    }
    bFetching = false;
  } catch (_error) {
    data = {
      "colr": "red",
      "icon": "exclamation",
      "titl": "WEB PANEL ERROR",
      "mess": _error.name
    }
    errorMessage(data);
    bFetching = false;
  }
}

async function prepareReq(_scriptname, _action, _file){
  if (bFetching)
    return;

  bFetching = true;

  if (_action == "prep")
    prepReq_init();
  else if (_action == "proc")
    procReq_init();

  sendReq(_scriptname, _action, _file);
}