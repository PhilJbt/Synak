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
function template_init() {
  $('#dp_loglevel').dropdown({
      allowCategorySelection: true,
      showOnFocus: false
  });
  $('#dp_loglevel').dropdown('set selected', '%LOGLEVEL%');
}
function sk_mng_strt() {
  bValidValues = true;
  arrOptVal = {};
  arrOptVal['lglv'] = $('#dp_loglevel_cnt')[0].firstChild.dataset.value.toString();
  arrOptVal['ptwp'] = $('#in_port_webpanel')[0].value;
  arrOptVal['ptpl'] = $('#in_port_players')[0].value;

  $('#in_port_webpanel')[0].classList.remove("inputError");
  if (/^\d+$/.test(arrOptVal['ptwp']) == false
  || arrOptVal['ptwp'].length == 0) {
    $('#in_port_webpanel')[0].classList.add("inputError");
    bValidValues = false;
  }

  $('#in_port_players')[0].classList.remove("inputError");
  if (/^\d+$/.test(arrOptVal['ptpl']) == false
  || arrOptVal['ptpl'].length == 0) {
    $('#in_port_players')[0].classList.add("inputError");
    bValidValues = false;
  }

  if (bValidValues)
    prepareReq('sk__req', 'proc', 'sk_mng_strt', JSON.stringify(arrOptVal));
  else
    $('.ui.modal').transition('bounce');
}
</script>