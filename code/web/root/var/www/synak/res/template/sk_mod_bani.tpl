<div class="header">
  Master Server &#8212; Ban IP
</div>
<div class="scrolling content">
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
      %BAN_ITEM%
    </div>
  </div>
</div>
<div class="actions">
  <div class="ui right aligned grid">
    <div class="left floated left aligned ten wide column middle aligned content">
      <i id="popnfo_modban" class="info help icon link"></i>
      <div class="ui top left popup flowing">
        <p>IPs can be <i>IPv4</i>, <i>IPv6</i> or <i>IPv4-mapped IPv6</i>.<br/>This feature uses <i>IPTABLES</i> which means IPs will be banned from all services hosted by this dedicated server (e.g. Synak Master Server, website).</p>
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
    $('#list_ipv4v6').append('%BAN_ITEM%');
  else if (_action == 'clr') {
    var objListIp = $('#list_ipv4v6').find('input');
    var iNbrChild = objListIp.length;
    for (var i = iNbrChild - 1; i >= 0; --i)
      if (objListIp[i].value.trim().length == 0
      && $('.rowban').length > 1)
        objListIp[i].parentNode.parentNode.parentNode.remove();
  }
}
function sk_mod_ban_send() {
  let rCheckIPv4v6 = /(?:^(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)){3}$)|(?:^(?:(?:[a-fA-F\d]{1,4}:){7}(?:[a-fA-F\d]{1,4}|:)|(?:[a-fA-F\d]{1,4}:){6}(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)(?:\\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)){3}|:[a-fA-F\d]{1,4}|:)|(?:[a-fA-F\d]{1,4}:){5}(?::(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)(?:\\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)){3}|(?::[a-fA-F\d]{1,4}){1,2}|:)|(?:[a-fA-F\d]{1,4}:){4}(?:(?::[a-fA-F\d]{1,4}){0,1}:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)(?:\\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)){3}|(?::[a-fA-F\d]{1,4}){1,3}|:)|(?:[a-fA-F\d]{1,4}:){3}(?:(?::[a-fA-F\d]{1,4}){0,2}:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)(?:\\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)){3}|(?::[a-fA-F\d]{1,4}){1,4}|:)|(?:[a-fA-F\d]{1,4}:){2}(?:(?::[a-fA-F\d]{1,4}){0,3}:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)(?:\\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)){3}|(?::[a-fA-F\d]{1,4}){1,5}|:)|(?:[a-fA-F\d]{1,4}:){1}(?:(?::[a-fA-F\d]{1,4}){0,4}:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)(?:\\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)){3}|(?::[a-fA-F\d]{1,4}){1,6}|:)|(?::(?:(?::[a-fA-F\d]{1,4}){0,5}:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)(?:\\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)){3}|(?::[a-fA-F\d]{1,4}){1,7}|:)))(?:%[0-9a-zA-Z]{1,})?$)/gm;
  listIPv4v6 = [];
  bValidValues = true;

  var objListIp = $('#list_ipv4v6').find('input');
  var iNbrChild = objListIp.length;
  for (var i = 0; i < iNbrChild; ++i) {
    if (!!objListIp[i].value.trim().length) {
      objListIp[i].classList.remove("inputError");
      if (!rCheckIPv4v6.test(objListIp[i].value.trim())) {
        objListIp[i].classList.add("inputError");
        bValidValues = false;
      }
      else
        listIPv4v6.push(objListIp[i].value.trim());
    }
  }

  if (!bValidValues)
    $('.ui.modal').transition('bounce');
  else if (listIPv4v6.length > 0)
    prepareReq('sk__req', 'proc', 'sk_mod_bani', JSON.stringify(listIPv4v6));
}
</script>