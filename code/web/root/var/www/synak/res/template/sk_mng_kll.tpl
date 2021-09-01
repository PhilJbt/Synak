<div class="header">
  Master Server &#8212; Kill Process
</div>
<div class="image content">
  <div class="description">
    <div class="ui header">Are you sure to KILL the Master Server main process?</div>
    <p>Process tree:</p>
    <pre>%VAR_1%</pre>
  </div>
</div>
<div class="actions">
<!--
  <div class="ui black deny left labeled icon button">
    Cancel
    <i class="arrow left icon"></i>
  </div>
  <div class="ui red right labeled icon button" onclick="prepareReq('sk__req', 'proc', 'sk_mng_kll')">
    Kill
    <i class="close icon"></i>
  </div>
-->
  <div class="ui animated button black deny">
    <div class="visible content">
      <i class="arrow left icon"></i>
    </div>
    <div class="hidden content">
      CANCEL
    </div>
  </div>
  <div id="btn_proceed" class="ui animated red button" onclick="prepareReq('sk__req', 'proc', 'sk_mng_kll')">
    <div class="visible content">
      <i class="icon close"></i>
    </div>
    <div class="hidden content">
      KILL
    </div>
  </div>
</div>