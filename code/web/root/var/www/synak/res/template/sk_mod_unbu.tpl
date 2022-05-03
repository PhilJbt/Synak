<div class="header">
  Master Server &#8212; Unban UID
</div>
<div class="content">
  <div class="description">
    <div class="ui header">Select UIDs to unban:</div>
    <h3>UID:</h3>
    <div id="listuid" class="ui middle aligned divided list">
      %UIDS%
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
  <div id="btn_proceed" class="ui animated green button" onclick="sk_mod_unb_pack()">
    <div class="visible content">
      <i class="icon check"></i>
    </div>
    <div class="hidden content">
      UNBAN
    </div>
  </div>
</div>
<script>
function template_init() {
  $('.ui.checkbox').checkbox();
}
function sk_mod_unb_pack() {
  listuid = [];

  var divListIPv4 = $('#listuid');
  var iNbrIPv4 = divListIPv4.find('input').length;
  for (var i = 0; i < iNbrIPv4; ++i)
    if ($('#listuid').find('input')[i].checked)
      listuid.push(divListIPv4.find('input')[i].getAttribute('data-uid'));

  if (listuid.length > 0)
    prepareReq('sk__req', 'proc', 'sk_mod_unbu', JSON.stringify(listuid));
}
</script>