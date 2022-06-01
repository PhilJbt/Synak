/*
** Run script when all the DOM is loaded
*/
window.addEventListener("load", function() {
  // Declare and initialize the variable blocking a feature request if another request is already loading
  window.bFetching = false;

  // Initializing the menu
  $('.accordion_menu').accordion();

  // Force disabling browser password prompt
  document.getElementById('inp_auth').onfocus = function() {
      document.getElementById('inp_auth').removeAttribute('readonly');
  };
  document.getElementById('inp_auth').onblur = function() {
      document.getElementById('inp_auth').setAttribute('readonly','readonly');
  };

  // Save permission key button bind
  document.getElementById('frm_auth').addEventListener('submit', function(event) {
      // Prevent sending the form
      event.preventDefault();

      // If the key input is not empty
      if ($('#inp_auth')[0].value.length == 0)
        return;

      // Disable the clicked button
      disablePermKeyButton();

      // Cast permission key from utf-8 to base64
      let authkeyEncrypted = btoa($('#inp_auth').val());
      // Store casted value to the input text
      $('#inp_auth').val(authkeyEncrypted);

      // Redirect to an url including the permission key
      window.location.href = `?permkey=${$('#inp_auth').val()}`;
  });

  // Check if is the url includes a permission key in order to pre-fill the permission key input text
  prefillPremKey();

  // If the user goes forward or backward in browser history
  $(window).on("popstate", function(e) {
    // Send a new request
    prewarmReq();
  });

  // Send a request if the url includes an action name
  prewarmReq();
});

/*
** Check if is the url includes a permission key in order to pre-fill the permission key input text
*/
function prefillPremKey() {
  // Get the permission key in the url
  let [paramChk, paramVal] = checkForUrlParam('permkey');
  // If the 'permkey' param exists
  if (paramChk) {
    // Fill the permission key input text with the param value
    $('#inp_auth').val(paramVal);
    // Disable and change the color of the permission key
    disablePermKeyButton();
  }
}

/*
** Initializing 'close' cross button of any messages elements
*/
function enableMessageClose() {
  // Bind all 'close' cross buttons included in a message element
  $('.message .close').on('click', function() {
    // With a fade animation
    $(this).closest('.message').transition('fade');
  });
}

/*
** Show error message received from the Python proxy
*/
function showErrorMessage(_error) {
  // Parse error message data array to HTML
  let strHtml = `<div class="ui icon message ${_error["colr"]}">\
  <i class="close icon"></i><i class="${_error["icon"]} icon"></i>\
  <div class="content"><div class="header"> ${_error["titl"]}</div>\
  <p>${_error["mess"]}</p>\
  </div></div>`;
  // Fill the text area with the parsed HTML
  $('#mdl_output').html(strHtml);
  // Disable the spinner of the output DOM container
  $('#mdl_output').removeClass("loading");
  // Enable 'close' cross button of the message element
  enableMessageClose();
}

/*
** Request Preparing Initialization
*/
function prepReq_beg() {
  // Enable the 'loading' class on the output DOM container
  $('#mdl_output').addClass("loading");
}

/*
** Request Preparing Uninitialization
*/
function prepReq_end(_text) {
  // Fill the modal with the received HTML
  $('.ui.modal').html(_text);
  // Set up options to the modal
  $('.ui.modal').modal({
    centered: false,
    transition: 'slide down'
  })
  // Show the modal
  .modal('show');
  // Disable the spinner on the output DOM container
  $('#mdl_output').removeClass("loading");
  // Enable 'close' cross button of the message element
  enableMessageClose();
  // Initialize custom javascript, if does exist
  templateInit_try();
}

/*
** Request Processing Initialization
*/
function procReq_beg() {
  // Enable the spinner on the 'Proceed' button of the modal
  $('#btn_proceed').addClass("loading");
  // Disable the 'Proceed' button of the modal
  $('#btn_proceed').addClass("disabled");
  // Enable the spinner on the output DOM container
  $('#mdl_output').addClass("loading");
}

/*
** Request Processing Uninitialization
*/
function procReq_end(_text) {
  // Fill the output DOM container with the HTML
  $('#mdl_output').html(_text);
  // Disable the spinner on the 'Proceed' button of the modal
  $('#btn_proceed').removeClass("loading");
  // Enable the 'Proceed' button of the modal
  $('#btn_proceed').removeClass("disabled");
  // Disable the spinner on the output DOM container
  $('#mdl_output').removeClass("loading");
  // Hide the modal
  $('.ui.modal').modal('hide');
  // Enable 'close' cross button of the message element
  enableMessageClose();
  // Initialize custom javascript, if does exist
  templateInit_try();
}

/*
** Request Error Message Uninitialization
*/
function errReq_end() {
  // Disable the spinner on the 'Proceed' button of the modal
  $('#btn_proceed').removeClass("loading");
  // Disable the 'Proceed' button of the modal
  $('#btn_proceed').removeClass("disabled");
  // Disable the spinner on the 'Proceed' button of the modal
  $('#mdl_output').removeClass("loading");
  // Hide the modal
  $('.ui.modal').modal('hide');
}

/*
** Change the current url
*/
function redirectUrl(_url) {
  // The history pushstate feature is supported by the browser
  if ("undefined" !== typeof history.pushState)
    // Change the current url without reloading the page
    history.pushState({}, null, `?permkey=${$('#inp_auth').val()}&action=${_url}`);
  // The history pushstate feature is not supported by the browser
  else
    // Proceed to a regular redirection
    window.location.assign(_url);
}

/*
** Check if a param exists in the current URL
*/
function checkForUrlParam(_param) {
  // Get the current URL
  const strQueryString = window.location.search;
  // Split each params into an array
  const arrUrlParams = new URLSearchParams(strQueryString);
  // The 'permkey' param exists
  if (arrUrlParams.get(_param) !== null) {
    // Return a tuple with the selected param
    return [true, arrUrlParams.get(_param)];
  }
  // The 'permkey' param does not exist
  else
    // Return a tuple with a null Data and a false 'Check
    return [false, null];
}

/*
** Proceed to a request if the url includes an action
*/
function prewarmReq() {
  // Get the 'action' URL param
  let [paramChk, paramVal] = checkForUrlParam('action');
  // If the 'action' URL param exists
  if (paramChk)
    // Send the corresponding request
    requestSend('sk__req', 'prep', paramVal);
}

/*
** Send the request to the Python proxy
*/
async function pythonProxyLiaison(_scriptname, _action, _file, _data = null) {
  // Erase the output DOM container content
  $('#mdl_output').html("");

  // Try to send the request
  try {
    // Set up the method, headers and body of the request
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
      'auth': $('#inp_auth').val()
      })
    }
    // Wait for the Python proxy answer
    const response = await fetch('res/python/' + _scriptname + '.py', config);
    // The answer is valid
    if (response.ok
      && response.status == 200) {
      // Cast the string to json
      let res = await response.json();
      // The data received is the first part of a request (i.e for user input, etc)
      if (res["type"] == "prep")
        // Send the data to be parsed
        prepReq_end(res["data"]);
      // The data received is the processing (i.e result of the request)
      else if (res["type"] == "proc")
        // Send the data to be parsed
        procReq_end(res["data"]);
      // The data received is an error message
      else if (res["type"] == "erro") {
        // Send the data to be parsed
        showErrorMessage(JSON.parse(res["data"]));
        // Uninitialization of the error message
        errReq_end();
      }
    }
    // The answer is not valid
    else {
      // Set up data for the error message
      data = {
        "colr": "red",
        "icon": "exclamation",
        "titl": "WEB PANEL ERROR",
        "mess": `Response status: ${response.status}.`
      }
      // Parse the error data and show the message
      showErrorMessage(data);
    }
    // Reactivate requests back
    window.bFetching = false;
  }
  // The request sending failed
  catch (_error) {
    // Set up data for the error message
    data = {
      "colr": "red",
      "icon": "exclamation",
      "titl": "WEB PANEL ERROR",
      "mess": `Error: ${_error.name}.`
    }
    // Parse the error data and show the message
    showErrorMessage(data);
    // Reactivate requests back
    window.bFetching = false;
  }
}

/*
** Formulate a request to be send
*/
async function requestSend(_scriptname, _action, _file, _data = null){
  // Exit the function if a request is already pending
  if (window.bFetching)
    return;
  // Else, disable requests
  else
    window.bFetching = true;

  // If the type of the answer is 'Preparation' (i.e for user input, etc)
  if (_action == "prep") {
    // Change DOM buttons and output containers with loading spinners or disabled attribute
    prepReq_beg();
    // Change the current URL corresponding to the requested type of action
    redirectUrl(_file);
  }
  // If the type of the answer is 'Processing' (i.e result of the request)
  else if (_action == "proc")
    // Change DOM buttons and output containers with loading spinners or disabled attribute
    procReq_beg();

  // Send the request to the Python proxy
  pythonProxyLiaison(_scriptname, _action, _file, _data);
}

/*
** Disable the 'Permission Key' button
*/
function disablePermKeyButton() {
  // Rename the value of the button
  $('#btn_auth').val("Applied");
  // Change the color of the button
  $('#btn_auth').addClass("green");
  // Disable the button
  $('#btn_auth').prop( "disabled", true );
  // Disable the text input
  $('#inp_auth').prop( "disabled", true );
}

/*
** Initialize custom javascript script in the HTML template, if does exist
*/
function templateInit_try() {
  // If the 'template_init' function exists
  if(typeof templateInit_run === "function")
    // Call the function included in the HTML template
    templateInit_run();
}