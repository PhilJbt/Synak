<div class="ui segment basic">
  <div class="ui buttons">
    <button id="btn_rld" class="ui labeled icon button blue" onclick="refreshPage(this)">
      <i class="icon sync alternate"></i>
      Reload
    </button>
    <button id="btn_era" class="ui labeled icon button red" onclick="eraseLog(this)">
      <i class="icon trash"></i>
      Erase Log
    </button>
  </div>
</div>
<div class="ui segment basic">
  <div class="ui accordion">
  %LOG%
  </div>
</div>
<script type="text/javascript">
function refreshPage(_this) {
  _this.disabled = true;
  _this.classList.add("loading");
  location.reload();
}
function eraseLog(_this) {
  _this.disabled = true;
  _this.classList.add("loading");
  prepareReq('sk__req', 'prep', 'sk_log_eras');
}
$('.ui.accordion').accordion();
</script>