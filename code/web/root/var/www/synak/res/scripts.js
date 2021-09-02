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
$('#popnfo_authkey').popup();
authKeyGet();

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
  template_try();
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

async function sendReq(_scriptname, _action, _file, _data = null) {
  $('#mdl_output').html("");

  var msauthkey = "";
  if (typeof(Storage) !== "undefined"
  && localStorage.getItem("msauthkey") !== null)
    msauthkey = localStorage.getItem("msauthkey");

  try {
    const config = {
      method: 'POST',
      headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({
      'type': _action,
      'data': (_data !== null ? _data : ''),
      'file': _file,
      'auth': msauthkey
      })
    }
    const response = await fetch('res/python/' + _scriptname + '.py', config);
    if (response.ok
      && response.status == 200) {
      var res = await response.json();
      //console.log(res["type"]);
      //console.log(res["data"]);
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

async function prepareReq(_scriptname, _action, _file, _data = null){
  if (bFetching)
    return;

  bFetching = true;

  if (_action == "prep")
    prepReq_init();
  else if (_action == "proc")
    procReq_init();

  sendReq(_scriptname, _action, _file, _data);
}

function authKeyErr() {
  data = {
      "colr": "red",
      "icon": "exclamation",
      "titl": "NEW BROWSER REQUIRED",
      "mess": "This browser is not supporting web local storage."
    }
    errorMessage(data);
}

function authKeySet() {
  if (typeof(Storage) !== "undefined") {
    localStorage.setItem("msauthkey", $('#in_authkey').val()); 
    $('#btn_save').text("Stored");
    $('#btn_save').addClass("green");
  }
  else
    authKeyErr();
}

function authKeyGet() {
  if (typeof(Storage) !== "undefined") {
    if (localStorage.getItem("msauthkey") !== null)
      $('#in_authkey').val(localStorage.getItem("msauthkey"));
  } else
    authKeyErr();
}

function template_try() {
  if(typeof template_init === "function")
    template_init();
}