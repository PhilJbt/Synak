<div class="header">
  Master Server &#8212; Unban IP
</div>
<div class="scrolling content">
  <div class="description">
    <div class="ui header">IPs to unban:</div>
    <div class="ui form">
      <textarea id="list_ipv4v6" placeholder="192.168.1.1&#10;2a01:cb1d:828a:7500:38f8:38da:e622:8711"></textarea>
    </div>
  </div>
</div>
<div class="actions">
  <div class="ui right aligned grid">
    <div class="left floated left aligned ten wide column middle aligned content">
      <i id="popnfo_modunban" class="info help icon link"></i>
      <div class="ui top left popup flowing">
        <p>Paste IPs to unban, one IP per line.<br/>IPs can be <i>IPv4</i>, <i>IPv6</i> or <i>IPv4-mapped IPv6</i>.</p>
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
function sk_mod_unban_send() {
  var objListIp = $('#list_ipv4v6')[0];
  listIPv4v6 = objListIp.value.split('\n');
  listIPv4v6 = listIPv4v6.filter(item => !(item.trim().length == 0));
  listIPv4v6.forEach((element, index) => {
    listIPv4v6[index] = element.replace(/\s+/g, ' ').trim();
  });

  if (listIPv4v6.length > 0)
    prepareReq('sk__req', 'proc', 'sk_mod_unbi', JSON.stringify(listIPv4v6));
}
</script>