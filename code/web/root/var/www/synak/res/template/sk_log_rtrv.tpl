<div class="ui segment basic">
  <div class="ui buttons">
    <button id="btn_rld" class="ui labeled icon button blue" onclick="refreshPage(this)">
      <i class="icon sync alternate"></i>
      Reload
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
$('.ui.accordion').accordion();
</script>