<div class="header">
  Master Server &#8212; Unban UID
</div>
<div class="content">
  <div class="description">
    <div class="ui buttons">
      <button class="ui button" onclick="sk_mod_unban_listuid('add')">
        <i class="plus icon"></i>
        ADD
      </button>
      <button class="ui button" onclick="sk_mod_unban_listuid('clr')">
        <i class="recycle icon"></i>
        CLEAR
      </button>
    </div>
    <div class="ui header">UID to unban:</div>
    <div id="list_uid">
      <div class="modunban ui icon input fluid">
        <input type="text" placeholder="UID to unban">
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
        <p>By default, the Synak UID (<i>Unique Identifier</i>) is the volume GUID, without brackets or dash (i.e. <i>{47ba2efc-3db1-11e0-78f8-806e5f6e6963}</i> becomes <i>47ba2efc3db111e078f8806e5f6e6963</i>).</p>
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
function sk_mod_unban_listuid(_action) {
  if (_action == 'add')
    $('#list_uid').append('<div class="modunban ui icon input fluid"><input type="text" placeholder="UID to unban"><i class="pencil alternate icon"></i></div>');
  else if (_action == 'clr') {
    var objListUid = $('#list_uid').find('input');
    var iNbrChild = objListUid.length;
    for (var i = iNbrChild - 1; i >= 0; --i)
      if (!objListUid[i].value.trim().length
      && ($('#list_uid').find('input').length > 1 || i > 0))
        objListUid[i].parentNode.remove();
  }
}
function sk_mod_unban_send() {
  listUid = [];

  var objListUid = $('#list_uid').find('input');
  var iNbrChild = objListUid.length;
  for (var i = 0; i < iNbrChild; ++i)
    if (!!objListUid[i].value.trim().length)
      listUid.push(objListUid[i].value.trim());

  if (listUid.length > 0)
    prepareReq('sk__req', 'proc', 'sk_mod_unbu', JSON.stringify(listUid));
}
</script>