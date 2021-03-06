<div class="header">
  Master Server &#8212; Kill Process
</div>
<div class="content">
  <div class="description">
    <div class="ui header">Are you sure to KILL the Master Server main process?</div>
    <p>Process tree:</p>
    <pre>%PROC_TREE%</pre>
  </div>
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
  <div id="btn_proceed" class="ui animated red button" onclick="requestSend('proc', 'sk_mng_kill')" tabindex="0">
    <div class="visible content">
      <i class="icon close"></i>
    </div>
    <div class="hidden content">
      KILL
    </div>
  </div>
</div>