$('.ui.dropdown').dropdown();

var bFetching = false;

function enableMessageClose() {
  $('.message .close').on('click', function() {
    $(this).closest('.message').transition('fade');
  });
}

function errorMessage(_error) {
  $('#mdl_output').removeClass("loading");    
  $('#mdl_output').html(
    '<div class="ui icon message '
    + _error["colr"] + '"><i class="close icon"></i><i class="'
    + _error["icon"] + ' icon"></i><div class="content"><div class="header">'
    + _error["titl"] + '</div><p>'
    + _error["mess"] + '</p></div></div>'
  );

  enableMessageClose();
}

function prepareReq_init() {
  $('#mdl_output').addClass("loading");
}

function prepareReq_uninit(_text) {
  $('.ui.modal').html(_text);
  $('.ui.modal').modal('show');
  $('#mdl_output').removeClass("loading");
  enableMessageClose();
}

function procReq_init() {
  $('.ui.modal').modal('show');
  $('#btn_proceed').addClass("loading");
  $('#mdl_output').addClass("loading");
}

function procReq_uninit(_text) {
  $('#mdl_output').html(_text);
  $('#btn_proceed').removeClass("loading");
  $('#mdl_output').removeClass("loading");
  enableMessageClose();
}

async function sendReq(_scriptname, _action) {
  try {
    const config = {
      method: 'POST',
      headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({
      'type': _action,
      'data': 'mydata'
      })
    }
    const response = await fetch('res/python/' + _scriptname + '.py', config);
    if (response.ok) {
      if (response.status == 200) {
        var res = await response.json();
        console.log(res["type"]);
        if (res["type"] == "prep") {
          //console.log(res["data"]);
          prepareReq_uninit(res["data"]);
        }
        else if (res["type"] == "proc")
          procReq_uninit(res["data"]);
        else if (res["type"] == "erro"){
          console.log(res["data"]);
          errorMessage(JSON.parse(res["data"]));
        }
      }
      bFetching = false;
    } else {
      data = {
        "colr": "red",
        "icon": "exclamation",
        "titl": "WEB PANEL ERROR",
        "mess": "unknown error"
      }
      errorMessage(data);
    }
  } catch (_error) {
    data = {
      "colr": "red",
      "icon": "exclamation",
      "titl": "WEB PANEL ERROR",
      "mess": _error.name
    }
    errorMessage(data);
  }
}

async function prepareReq(_scriptname, _action){
  bFetching = true;

  if (_action == "get")
    prepareReq_init();
  else if (_action == "set")
    procReq_init();

  sendReq(_scriptname, _action);
}