<div class="header">
  Master Server &#8212; Unban UID
</div>
<div class="scrolling content">
  <div class="description">
    <div class="ui header">UID to unban:</div>
    <div class="ui form">
      <textarea id="list_uid" placeholder="a6a5e426-e06a-4d32-8b8a-83234f367b4d&#10;81e5a262-5027-4b5a-b5d8-4f87c75568ee"></textarea>
      <div id="tip_uid" class="ui pointing label basic red" style="opacity:0">
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
        <p>Paste one UID per line, separate the ban duration in days with a space.<br/>By default, the Synak UID (<i>Unique Identifier</i>) is the volume GUID (i.e. <i>{47ba2efc-3db1-11e0-78f8-806e5f6e6963}</i>).</p>
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
<script type="text/javascript">
function templateInit_run() {
  $('#popnfo_info').popup({
    variation : 'very wide'
  });
  $('#popnfo_linenbr').popup({
    variation : 'very wide'
  });
  $('#list_uid').on('input', function() {
    tipUpdate();
  });
}
function tipUpdate() {
  let nbrLines = $('#list_uid')[0].value.split("\n").length;

  $('#popnfo_linenbr')[0].classList.remove('black');
  $('#popnfo_linenbr')[0].classList.remove('red');
  $('#popnfo_linenbr')[0].classList.remove('orange');
  $('#popnfo_linenbr')[0].classList.remove('yellow');
  $('#popnfo_linenbr')[0].classList.remove('green');

  $('#popnfo_linenbr')[0].innerHTML = nbrLines.toString();

  $('#tip_uid')[0].innerHTML = 'Null';
  $('#tip_uid')[0].style.opacity = 0;

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
function sk_mod_unban_send() {
  var objlistUid = $('#list_uid')[0];
  listUIDs = objlistUid.value.split('\n');
  listUIDs = listUIDs.filter(item => !(item.trim().length == 0));
  listUIDs.forEach((element, index) => {
    listUIDs[index] = element.replace(/\s+/g, ' ').trim();
  });

  if (listUIDs.length > 0)
    requestSend('proc', 'sk_mod_unbu', JSON.stringify(listUIDs));
  else {
    $('#tip_uid')[0].innerHTML = 'Error : No entry filled';
    $('#tip_uid')[0].style.opacity = 1;
    $('.ui.modal').transition('bounce');
  }
}
</script>