<div class="header">
  Master Server &#8212; Options
</div>
<div class="content">
  <div class="description">
    <div class="ui header">Options available to apply for the Synak Master Server:</div>

    <div class="ui sub header">Log level</div>
    <div id="dp_loglevel" class="ui dropdown button">
      <span id="dp_loglevel_cnt" class="text">Choose Category</span>
      <i class="dropdown icon"></i>
      <div class="menu">
        <div data-value="2" class="item">
          <span data-value="2" class="text"><i class="icon exclamation triangle red"></i> Errors</span>
        </div>
        <div data-value="1" class="item">
          <span data-value="1" class="text"><i class="icon exclamation circle orange"></i> Warnings</span>
        </div>
        <div data-value="0" class="item">
          <span data-value="0" class="text"><i class="icon info circle blue"></i> Informations</span>
        </div>
        </div>
      </div>
    </div>

  </div>
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
  <div id="btn_proceed" class="ui animated green button" onclick="prepareReq('sk__req', 'proc', 'sk_mng_optn')">
    <div class="visible content">
      <i class="icon check"></i>
    </div>
    <div class="hidden content">
      APPLY
    </div>
  </div>
</div>
<script type="text/javascript">
$('#dp_loglevel')
  .dropdown({
    allowCategorySelection: true,
    showOnFocus: false
  })
;
$("#dp_loglevel_cnt")[0].firstChild.dataset.value;
</script>