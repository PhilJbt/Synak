<div class="header">
  Master Server &#8212; List of banned IPs
</div>
<div class="content">
  <div class="description">
    <div class="ui header">Banned IPs:</div>
    <div id="listipv4" class="ui middle aligned divided list">
      %IPV4%
    </div>
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
      CLOSE
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
    prepareReq('sk__req', 'proc', 'sk_mod_unbi', JSON.stringify(listIPv4v6));
}
</script>