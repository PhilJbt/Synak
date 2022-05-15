<div class="header">
  Master Server &#8212; Ban UID
</div>
<div class="scrolling content">
  <div class="description">
    <div class="ui header">UIDs to ban:</div>
    <div class="ui form">
      <textarea id="list_uid" placeholder="a6a5e426-e06a-4d32-8b8a-83234f367b4d 7&#10;81e5a262-5027-4b5a-b5d8-4f87c75568ee 365"></textarea>
    </div>
  </div>
</div>
<div class="actions">
  <div class="ui right aligned grid">
    <div class="left floated left aligned ten wide column middle aligned content">
      <i id="popnfo_modban" class="info help icon link"></i>
      <div class="ui top left popup flowing">
        <p>Paste one UID per line, separate the ban duration in days with a space.<br/>By default, the Synak UID (<i>Unique Identifier</i>) is the volume GUID (i.e. <i>{47ba2efc-3db1-11e0-78f8-806e5f6e6963}</i>).</p>
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
  listUid = [];

  var objListUid = $('#list_uid')[0];
  listIPv4v6 = objListUid.value.split('\n');
  for (let i = 0; i < listIPv4v6.length; ++i) {
    const element = listIPv4v6[i].replace(/\s+/g, ' ').trim();
    if (element.length > 0) {
      if ((element.match(/ /g)||[]).length != 1) {
        $('.ui.modal').transition('bounce');
        return;
      }
      else {
        let strLine = element.split(' ');
        arrTmp = [];
        arrTmp.push(strLine[0]);
        arrTmp.push(strLine[1]);
        listUid.push(arrTmp);
      }
    }
  }

  if (listUid.length > 0)
    prepareReq('sk__req', 'proc', 'sk_mod_banu', JSON.stringify(listUid));
}
</script>