<div class="header">
  Master Server &#8212; Options
</div>
<div class="content">
  <div class="ui header">Options available to apply for the Synak Master Server:</div>
  %FORM_OPT_GLOBAL%
</div>
<div class="actions">
  <div class="ui animated button black deny" tabindex="0">
    <div class="visible content">
      <i class="arrow left icon"></i>
    </div>
    <div class="hidden content">
      CANCEL
    </div>
  </div>
  <div id="btn_proceed" class="ui animated green button" onclick="sk_mng_optn()" tabindex="0">
    <div class="visible content">
      <i class="icon check"></i>
    </div>
    <div class="hidden content">
      APPLY
    </div>
  </div>
</div>
<script type="text/javascript">
function templateInit_run() {
  $('#dp_loglevel').dropdown({
      allowCategorySelection: true,
      showOnFocus: false
  });
  $('#dp_loglevel').dropdown('set selected', %LGLV%);
}
function sk_mng_optn() {
  arrOptVal = {};
  arrOptVal['lglv'] = $('#dp_loglevel_cnt')[0].firstChild.dataset.value.toString();
  requestSend('proc', 'sk_mng_optn', JSON.stringify(arrOptVal));
}
</script>