<div class="header">
  Master Server &#8212; Start
</div>
<div class="content">
  <div class="ui header">Options available for startup:</div>
  %FORM_OPT_START%
  %FORM_OPT_GLOBAL%
</div>
<div class="actions">
  <div class="ui animated button black deny">
    <div class="visible content">
      <i class="arrow left icon"></i>
    </div>
    <div class="hidden content">
      CANCEL
    </div>
  </div>
  <div id="btn_proceed" class="ui animated green button" onclick="sk_mng_strt()">
    <div class="visible content">
      <i class="icon play"></i>
    </div>
    <div class="hidden content">
      START
    </div>
  </div>
</div>
<script type="text/javascript">
function templateInit_run() {
  $('#dp_loglevel').dropdown({
      allowCategorySelection: true,
      showOnFocus: false
  });
  $('#dp_loglevel').dropdown('set selected', '%LOGLEVEL%');
}
function sk_mng_strt() {
  arrOptVal = {};
  arrOptVal['lglv'] = $('#dp_loglevel_cnt')[0].firstChild.dataset.value.toString();
  arrOptVal['ptwp'] = $('#in_port_webpanel')[0].value;
  arrOptVal['ptpl'] = $('#in_port_players')[0].value;

  hideErrPop($('#popup_port_webpanel')[0]);
  if (arrOptVal['ptwp'].length == 0) {
    showErrPop($('#popup_port_webpanel')[0], 'Please fill in a port number.');
    $('.ui.modal').transition('bounce');
    return;
  }
  else if (parseInt(arrOptVal['ptwp']) == 0) {
    showErrPop($('#popup_port_webpanel')[0], 'Bind port 0 will use a random port number, which is not desirable for a public server.');
    $('.ui.modal').transition('bounce');
    return;
  }
  else if (/^\d+$/.test(arrOptVal['ptwp']) == false) {
    showErrPop($('#popup_port_webpanel')[0], 'This value has to be a number.');
    $('.ui.modal').transition('bounce');
    return;
  }

  hideErrPop($('#popup_port_players')[0]);
  if (arrOptVal['ptpl'].length == 0) {
    showErrPop($('#popup_port_players')[0], 'Please fill in a port number.');
    $('.ui.modal').transition('bounce');
    return;
  }
  else if (parseInt(arrOptVal['ptpl']) == 0) {
    showErrPop($('#popup_port_players')[0], 'Bind port 0 will use a random port number, which is not desirable for a public server.');
    $('.ui.modal').transition('bounce');
    return;
  }
  else if (/^\d+$/.test(arrOptVal['ptpl']) == false) {
    showErrPop($('#popup_port_players')[0], 'This value has to be a number.');
    $('.ui.modal').transition('bounce');
    return;
  }

  requestSend('sk__req', 'proc', 'sk_mng_strt', JSON.stringify(arrOptVal));
}
</script>