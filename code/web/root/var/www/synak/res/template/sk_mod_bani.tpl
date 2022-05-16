<div class="header">
  Master Server &#8212; Ban IP
</div>
<div class="scrolling content">
  <div class="description">
    <div class="ui header">IPs to ban:</div>
    <div class="ui form">
      <textarea id="list_ipv4v6" placeholder="192.168.1.1&#10;2a01:cb1d:828a:7500:38f8:38da:e622:8711"></textarea>
      <div id="tip_ip" class="ui pointing label basic red" style="opacity:0">
        Null
      </div>
    </div>
  </div>
</div>
<div class="actions">
  <div class="ui right aligned grid">
    <div class="left floated left aligned ten wide column middle aligned content">
      <i id="popnfo_info" class="info help icon link"></i>
      <div class="ui top left popup flowing">
        <p>Paste IPs to ban, one IP per line.<br/>IPs can be <i>IPv4</i>, <i>IPv6</i> or <i>IPv4-mapped IPv6</i>.<br/>This feature uses <i>IPTABLES</i> which means IPs will be banned from all services hosted by this dedicated server (e.g. Synak Master Server, website).</p>
      </div>
      <a id="popnfo_linenbr" class="ui label circular green">1</a>
      <div class="ui top left popup flowing">
        <p id="popnfo_process">Will be processed quickly.</p>
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
  $('#popnfo_info').popup({
    variation : 'very wide'
  });
  $('#popnfo_linenbr').popup({
    variation : 'very wide'
  });
  $('#list_ipv4v6').on('input', function() {
    tipUpdate();
  });
}
function tipUpdate() {
  let nbrLines = $('#list_ipv4v6')[0].value.split("\n").length;

  $('#popnfo_linenbr')[0].classList.remove('black');
  $('#popnfo_linenbr')[0].classList.remove('red');
  $('#popnfo_linenbr')[0].classList.remove('orange');
  $('#popnfo_linenbr')[0].classList.remove('yellow');
  $('#popnfo_linenbr')[0].classList.remove('green');

  $('#popnfo_linenbr')[0].innerHTML = nbrLines.toString();

  $('#tip_ip')[0].innerHTML = 'Null';
  $('#tip_ip')[0].style.opacity = 0;

  if (nbrLines >= 200) {
    $('#popnfo_linenbr')[0].classList.add('black');
    $('#popnfo_process')[0].innerHTML = 'Will take time to be processed.';
  }
  else if (nbrLines >= 150) {
    $('#popnfo_linenbr')[0].classList.add('red');
    $('#popnfo_process')[0].innerHTML = 'May take some time to be processed.';
  }
  else if (nbrLines >= 100) {
    $('#popnfo_linenbr')[0].classList.add('orange');
    $('#popnfo_process')[0].innerHTML = 'Should not take too long to be processed.';
  }
  else if (nbrLines >= 50) {
    $('#popnfo_linenbr')[0].classList.add('yellow');
    $('#popnfo_process')[0].innerHTML = 'Should be processed quickly.';
  }
  else {
    $('#popnfo_linenbr')[0].classList.add('green');
    $('#popnfo_process')[0].innerHTML = 'Will be processed quickly.';
  }
}
function sk_mod_ban_send() {
  var objListIp = $('#list_ipv4v6')[0];
  listIPv4v6 = objListIp.value.split('\n');
  listIPv4v6 = listIPv4v6.filter(item => !(item.trim().length == 0));
  if (listIPv4v6.length > 0)
    prepareReq('sk__req', 'proc', 'sk_mod_bani', JSON.stringify(listIPv4v6));
  else {
    $('#tip_ip')[0].innerHTML = 'Error : No entry filled';
    $('#tip_ip')[0].style.opacity = 1;
    $('.ui.modal').transition('bounce');
  }
}
</script>