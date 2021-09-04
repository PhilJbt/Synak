<div class="header">
  Master Server &#8212; Ban IP
</div>
<div class="content">
  <div class="description">
    <div class="ui buttons">
      <button class="ui button" onclick="sk_mod_ban_listip('add')">
        <i class="plus icon"></i>
        ADD
      </button>
      <button class="ui button" onclick="sk_mod_ban_listip('clr')">
        <i class="recycle icon"></i>
        CLEAR
      </button>
    </div>
    <div class="ui header">IP to ban:</div>
    <div id="list_ipv4v6">
      <div class="modban ui icon input fluid">
        <input type="text" placeholder="IP to ban">
        <i class="pencil alternate icon"></i>
      </div>
    </div>
  </div>
</div>
<div class="actions">
  <div class="ui right aligned grid">
    <div class="left floated left aligned ten wide column middle aligned content">
      <i id="popnfo_modban" class="info help icon link"></i>
      <div class="ui top left popup flowing">
        <p>IPs can be <i>IPv4</i>, <i>IPv6</i> or <i>IPv4-mapped IPv6</i>.<br/>This feature uses <i>IPTABLES</i> which means IPs will be banned from all services hosted by this dedicated server (e.g. Synak Master Server, web).</p>
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
      <div id="btn_proceed" class="ui animated red button" onclick="sk_mod_ban_send()">
        <div class="visible content">
          <i class="icon ban"></i>
        </div>
        <div class="hidden content">
          BAN
        </div>
      </div>
    </div>
  </div>
</div>
<script>
function template_init() {
  $('#popnfo_modban').popup({
    variation : 'very wide'
  });
}
function sk_mod_ban_listip(_action) {
  if (_action == 'add')
    $('#list_ipv4v6').append('<div class="modban ui icon input fluid"><input type="text" placeholder="IP to ban"><i class="pencil alternate icon"></i></div>')
  else if (_action == 'clr') {
    var objListIp = $('#list_ipv4v6').find('input');
    var iNbrChild = objListIp.length;
    for (var i = iNbrChild - 1; i >= 0; --i)
      if (!objListIp[i].value.trim().length
      && ($('#list_ipv4v6').find('input').length > 1 || i > 0))
        objListIp[i].parentNode.remove();
  }
}
function sk_mod_ban_send() {
  listIPv4v6 = [];

  var objListIp = $('#list_ipv4v6').find('input');
  var iNbrChild = objListIp.length;
  for (var i = 0; i < iNbrChild; ++i)
    if (!!objListIp[i].value.trim().length)
      listIPv4v6.push(objListIp[i].value.trim());

  if (listIPv4v6.length > 0)
    prepareReq('sk__req', 'proc', 'sk_mod_ban', JSON.stringify(listIPv4v6));
}
</script>