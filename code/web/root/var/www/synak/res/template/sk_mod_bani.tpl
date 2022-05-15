<div class="header">
  Master Server &#8212; Ban IP
</div>
<div class="scrolling content">
  <div class="description">
    <div class="ui header">IPs to ban:</div>
    <div class="ui form">
      <textarea id="list_ipv4v6" placeholder="192.168.1.1&#10;2a01:cb1d:828a:7500:38f8:38da:e622:8711"></textarea>
    </div>
  </div>
</div>
<div class="actions">
  <div class="ui right aligned grid">
    <div class="left floated left aligned ten wide column middle aligned content">
      <i id="popnfo_modban" class="info help icon link"></i>
      <div class="ui top left popup flowing">
        <p>Paste IPs to ban, one IP per line.<br/>IPs can be <i>IPv4</i>, <i>IPv6</i> or <i>IPv4-mapped IPv6</i>.<br/>This feature uses <i>IPTABLES</i> which means IPs will be banned from all services hosted by this dedicated server (e.g. Synak Master Server, website).</p>
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
function sk_mod_ban_send() {
  var objListIp = $('#list_ipv4v6')[0];
  listIPv4v6 = objListIp.value.split('\n');
  listIPv4v6 = listIPv4v6.filter(item => !(item.trim().length == 0));
  if (listIPv4v6.length > 0)
    prepareReq('sk__req', 'proc', 'sk_mod_bani', JSON.stringify(listIPv4v6));
}
</script>