<div class="header">
  Master Server &#8212; Unban IP
</div>
<div class="scrolling content">
  <div class="description">
    <div class="ui buttons">
      <button class="ui button" onclick="sk_mod_unban_listip('add')">
        <i class="plus icon"></i>
        ADD
      </button>
      <button class="ui button" onclick="sk_mod_unban_listip('clr')">
        <i class="recycle icon"></i>
        CLEAR
      </button>
    </div>
    <div class="ui header">IP to unban:</div>
    <div id="list_ipv4v6">
      <div class="modunban ui icon input fluid">
        <input type="text" placeholder="IP to unban">
        <i class="pencil alternate icon"></i>
      </div>
    </div>
  </div>
</div>
<div class="actions">
  <div class="ui right aligned grid">
    <div class="left floated left aligned ten wide column middle aligned content">
      <i id="popnfo_modunban" class="info help icon link"></i>
      <div class="ui top left popup flowing">
        <p>IPs can be <i>IPv4</i>, <i>IPv6</i> or <i>IPv4-mapped IPv6</i>.<br/>This feature uses <i>IPTABLES</i> which means IPs will be unbanned from all services hosted by this dedicated server (e.g. Synak Master Server, website).</p>
      </div>
    </div>
    <div class="right floated right aligned six wide column">
      <div class="ui animated button black deny">
        <div class="visible content">
          <i class="arrow left icon"></i>
        </div>
        <div class="hidden content">
          CANCEL
        </div>
      </div>
      <div id="btn_proceed" class="ui animated green button" onclick="sk_mod_unban_send()">
        <div class="visible content">
          <i class="icon check"></i>
        </div>
        <div class="hidden content">
          UNBAN
        </div>
      </div>
    </div>
  </div>
</div>
<script>
function template_init() {
  $('#popnfo_modunban').popup({
    variation : 'very wide'
  });
}
function sk_mod_unban_listip(_action) {
  if (_action == 'add')
    $('#list_ipv4v6').append('<div class="modunban ui icon input fluid"><input type="text" placeholder="IP to unban"><i class="pencil alternate icon"></i></div>');
  else if (_action == 'clr') {
    var objListIp = $('#list_ipv4v6').find('input');
    var iNbrChild = objListIp.length;
    for (var i = iNbrChild - 1; i >= 0; --i)
      if (!objListIp[i].value.trim().length
      && ($('#list_ipv4v6').find('input').length > 1 || i > 0))
        objListIp[i].parentNode.remove();
  }
}
function sk_mod_unban_send() {
  listIPv4v6 = [];

  var objListIp = $('#list_ipv4v6').find('input');
  var iNbrChild = objListIp.length;
  for (var i = 0; i < iNbrChild; ++i)
    if (!!objListIp[i].value.trim().length)
        listIPv4v6.push(objListIp[i].value.trim());

  if (listIPv4v6.length > 0)
    prepareReq('sk__req', 'proc', 'sk_mod_unbi', JSON.stringify(listIPv4v6));
}
</script>