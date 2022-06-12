/*
** Run script when all the DOM is loaded
*/
window.addEventListener("load", function() {
  // Show the disclaimer in the console
  console.log("%c%s",'color: #FF0000; font-size: 50px;font-family:"Roboto", Arial, sans-serif;font-weight:bold;',"WARNING");
  console.log("READ BEFORE DOING ANYTHING: If someone has invited you to copy and paste something here, whatever the reason, be aware that this may allow the person in question to run the Master Server or Dedicated Server/VPS scripts.");

  /*
  ** Press the 'Enter' key to click the focused button
  */
  $(document).keydown(function(event) {
    if (!window.bFetching
    && event.which === 13) {
      if (document.activeElement.classList.contains('ui')
        && document.activeElement.classList.contains('button')
        && typeof document.activeElement.click === "function")
        document.activeElement.click();
    }
  });

  // Declare and initialize the variable blocking a feature request if another request is already loading
  window.bFetching = false;

  // Initializing the menu
  $('.accordion_menu').accordion();

  // Bind the forward and backward browser history move
  $(window).on("popstate", function(e) {
    // Send a new request
    prewarmReq();
  });

  // Check for credential cookie
  let bCredFound = credentialCookie_Check();

  // Send a request if the url includes an action name
  if (bCredFound)
    prewarmReq();
});

/*
** Show the login modal and ask for credential if credential cookie does not exist
*/
function credentialCookie_Check() {
  // Split the cookie string into an array
  let arrCred = document.cookie.split(';');
  // Declare and initialize the credentials dictionnary
  let dicCred = {};
  // For every cookie argument
  arrCred.forEach(function(elem) {
    // If the string element includes an equal sign
    if (elem.includes('=')) {
      // Split the string element in half
      let arrTempSplit = elem.split('=');
      // If the string element has two parts
      if (arrTempSplit.length == 2)
        // Save the first and second part in the credential dictionnary
        dicCred[arrTempSplit[0].trim()] = arrTempSplit[1].trim();
    }
  });

  // If 'sk_log' or 'sk_pwd' does not exist in the credential cookie
  if (!('sk_log' in dicCred)
    || !('sk_pwd' in dicCred)) {
    // Set up options to the modal
    $('#mdl_cred').modal({
      closable: false,
      transition: 'vertical flip'
    })
    // Show the modal
    .modal('show');
  }
  // Credential cookie is well populated
  else
    return true;
}

/*
** SHA-256 string encryption
*/
async function cryptString(message) {
  // Encode as (utf-8) Uint8Array
  const msgUint8 = new TextEncoder().encode(message);
  // Hash the message
  const hashBuffer = await crypto.subtle.digest('SHA-256', msgUint8);
  // Convert buffer to byte array
  const hashArray = Array.from(new Uint8Array(hashBuffer))
  // Convert bytes to hex string
  const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
  return hashHex;
}

/*
** Bind 'Login' button with ajax login
*/
document.getElementById('btn_login').addEventListener('click', event => {
  // Prevent the form submission
  event.preventDefault();

  // Run ajax login
  credentialCookie_Set();
});

/*
** Credential modal login
*/
async function credentialCookie_Set() {
  // Cancel the credential set if the login or the password input text is empty
  if ($('#sk_log')[0].value.length == 0
  || $('#sk_pwd')[0].value.length == 0)
    return;

  // Encrypt password
  const digestHexPasswd = await cryptString($('#sk_pwd')[0].value.toString() + 'SYNAK_wp');

  // Save the credential cookie
  document.cookie = `sk_log=${$('#sk_log')[0].value}`;
  document.cookie = `sk_pwd=${digestHexPasswd}`;

  // Erase the content of login and password text input
  $('#sk_log')[0].value = "";
  $('#sk_pwd')[0].value = "";

  // Hide the credentials modal
  $('#mdl_cred').modal('hide');

  // Proceed to a request if the url includes an action
  prewarmReq();
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
  $('#mdl_cont').html(_text);
  // Set up options to the modal
  $('#mdl_cont').modal({
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
  $('#mdl_cont').modal('hide');
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
  $('#mdl_cont').modal('hide');
}

/*
** Change the current url
*/
function redirectUrl(_url) {
  // The history pushstate feature is supported by the browser
  if ("undefined" !== typeof history.pushState)
    // Change the current url without reloading the page
    history.pushState({}, null, `?action=${_url}`);
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
    requestSend('prep', paramVal);
}

/*
** Send the request to the Python proxy
*/
async function pythonProxyLiaison(_action, _file, _data = null) {
  // Erase the output DOM container content
  $('#mdl_output').html("");

  // Try to send the request
  try {
    // Set up the method, headers and body of the request
    const config = {
      method: 'POST',
      headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        'type': _action,
        'data': (_data !== null ? _data : ''),
        'file': _file
      }),
      credentials: 'include'
    }
    // Wait for the Python proxy answer
    const response = await fetch('res/python/sk__req.cgi', config);
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
async function requestSend(_action, _file, _data = null){
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
  pythonProxyLiaison(_action, _file, _data);
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