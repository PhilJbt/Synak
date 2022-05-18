<div class="header">
  Master Server &#8212; Ban UID
</div>
<div class="scrolling content">
  <div class="description">
    <div class="ui header">UIDs to ban:</div>
    <div class="ui form">
      <textarea id="list_uid" placeholder="a6a5e426-e06a-4d32-8b8a-83234f367b4d 7&#10;81e5a262-5027-4b5a-b5d8-4f87c75568ee 365"></textarea>
      <div id="tip_uid" class="ui pointing label basic red popuperr">
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
function selectError(_start, _offset) {
	var txtArea = $('#list_uid')[0];
	txtArea.focus();
	txtArea.selectionStart = _start;
	txtArea.selectionEnd = _start + _offset;
}
function sk_mod_ban_send() {
  listUid = [];

  let nbrChar = 0;
  var objListUid = $('#list_uid')[0];
  listIPv4v6 = objListUid.value.split('\n');
  for (let i = 0; i < listIPv4v6.length; ++i) {
    const element = listIPv4v6[i].replace(/\s+/g, ' ').trim();
    if (element.length > 0) {
      if ((element.match(/ /g)||[]).length != 1) {
        $('#tip_uid')[0].innerHTML = `Error : there is no space character at line ${(i+1).toString()}.`;
        $('#tip_uid')[0].style.opacity = 1;
        selectError(nbrChar, element.length + 1);
        $('.ui.modal').transition('bounce');
        return;
      }
      else {
        let strLine = element.split(' ');
        if (/^\d+$/.test(strLine[1])) {
          arrTmp = [];
          arrTmp.push(strLine[0]);
          arrTmp.push(strLine[1]);
          listUid.push(arrTmp);
        }
        else {
          $('#tip_uid')[0].innerHTML = `Error : the number of ban days at line ${(i+1).toString()} is not a valid number.`;
          $('#tip_uid')[0].style.opacity = 1;
          selectError(nbrChar + strLine[0].length + 2, strLine[1].length + 1);
          $('.ui.modal').transition('bounce');
          return;
        }
      }
    }
    nbrChar += element.length;
  }

  if (listUid.length > 0)
    prepareReq('sk__req', 'proc', 'sk_mod_banu', JSON.stringify(listUid));
  else {
    $('#tip_uid')[0].innerHTML = 'Error : No entry filled.';
    $('#tip_uid')[0].style.opacity = 1;
    $('.ui.modal').transition('bounce');
  }
}
</script>