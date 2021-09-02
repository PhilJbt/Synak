<div class="header">
  Master Server &#8212; Unban IP
</div>
<div class="content">
  <div class="description">
    <div class="ui header">Select IPs to unban:</div>
    <h3>IPv4:</h3>
    <div id="listipv4" class="ui middle aligned divided list">
      %IPV4%
    </div>
    <h3>IPv6:</h3>
    <div id="listipv6" class="ui middle aligned divided list">
      %IPV6%
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
  listIPv4v6 = [];

  var divListIPv4 = $('#listipv4');  
  var iNbrIPv4 = divListIPv4.find('input').length;
  for (var i = 0; i < iNbrIPv4; ++i)
    if ($('#listipv4').find('input')[i].checked)
      listIPv4v6.push(divListIPv4.find('input')[i].getAttribute('data-ip'));

  var divListIPv6 = $('#listipv6');
  var iNbrIPv6 = divListIPv6.find('input').length;
  for (var i = 0; i < iNbrIPv6; ++i)
    if ($('#listipv6').find('input')[i].checked)
      listIPv4v6.push(divListIPv6.find('input')[i].getAttribute('data-ip'));

  if (listIPv4v6.length > 0)
    prepareReq('sk__req', 'proc', 'sk_mod_unb', JSON.stringify(listIPv4v6));
}
</script>