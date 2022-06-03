<div class="header">
  Master Server &#8212; Erase log
</div>
<div class="content">
  <div class="description">
    Are you sure to erase the Synak Master Server log file ?
  </div>
</div>
<div class="actions">
  <div class="ui right aligned grid">
    <div class="right floated right aligned six wide column">
      <div class="ui animated button black deny">
        <div class="visible content">
          <i class="arrow left icon"></i>
        </div>
        <div class="hidden content">
          CANCEL
        </div>
      </div>
      <div id="btn_proceed" class="ui animated red button" onclick="sk_log_eras()">
        <div class="visible content">
          <i class="icon trash"></i>
        </div>
        <div class="hidden content">
          ERASE
        </div>
      </div>
    </div>
  </div>
</div>
<script type="text/javascript">
function templateInit_run() {
  $('#popnfo_modban').popup({
    variation : 'very wide'
  });
}
function sk_log_eras() {
  requestSend('proc', 'sk_log_eras', '');
}
</script>