<div class="header">
  Master Server &#8212; Unban UID
</div>
<div class="scrolling content">
  <div class="description">
    <div class="ui header">UID to unban:</div>
    <div class="ui form">
      <textarea id="list_uid" placeholder="a6a5e426-e06a-4d32-8b8a-83234f367b4d&#10;81e5a262-5027-4b5a-b5d8-4f87c75568ee"></textarea>
    </div>
  </div>
</div>
<div class="actions">
  <div class="ui right aligned grid">
    <div class="left floated left aligned ten wide column middle aligned content">
      <i id="popnfo_modunban" class="info help icon link"></i>
      <div class="ui top left popup flowing">
        <p>Paste one UID per line.<br/>By default, the Synak UID (<i>Unique Identifier</i>) is the volume GUID (i.e. <i>{47ba2efc-3db1-11e0-78f8-806e5f6e6963}</i>).</p>
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
  var objlistUid = $('#list_uid')[0];
  listUIDs = objlistUid.value.split('\n');
  listUIDs = listUIDs.filter(item => !(item.trim().length == 0));
  listUIDs.forEach((element, index) => {
    listUIDs[index] = element.replace(/\s+/g, ' ').trim();
  });

  if (listUIDs.length > 0)
    prepareReq('sk__req', 'proc', 'sk_mod_unbu', JSON.stringify(listUIDs));
}
</script>