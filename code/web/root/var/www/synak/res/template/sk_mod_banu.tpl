<div class="header">
  Master Server &#8212; Ban UID
</div>
<div class="scrolling content">
  <div class="description">
    <div class="ui buttons">
      <button class="ui button" onclick="sk_mod_ban_listuid('add')">
        <i class="plus icon"></i>
        ADD
      </button>
      <button class="ui button" onclick="sk_mod_ban_listuid('clr')">
        <i class="recycle icon"></i>
        CLEAR
      </button>
    </div>
    <div class="ui header">UID to ban:</div>
    <div id="list_uid">
      %BAN_ITEM%
    </div>
  </div>
</div>
<div class="actions">
  <div class="ui right aligned grid">
    <div class="left floated left aligned ten wide column middle aligned content">
      <i id="popnfo_modban" class="info help icon link"></i>
      <div class="ui top left popup flowing">
        <p>By default, the Synak UID (<i>Unique Identifier</i>) is the volume GUID (i.e. <i>{47ba2efc-3db1-11e0-78f8-806e5f6e6963}</i>).</p>
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
function sk_mod_ban_listuid(_action) {
  if (_action == 'add')
    $('#list_uid').append('%BAN_ITEM%');
  else if (_action == 'clr') {
    var objListUid = $('#list_uid').find('.nptban');
    var iNbrChild = objListUid.length;
    for (var i = iNbrChild - 1; i >= 0; --i)
      if (objListUid[i].value.trim().length == 0
      && $('.rowban').length > 1)
        objListUid[i].parentNode.parentNode.parentNode.parentNode.remove();
  }
}
function sk_mod_ban_send() {
  listUid = [];
  bValuesValid = true;

  var objListUid = $('.rowban');
  var iNbrChild = objListUid.length;
  for (var i = 0; i < iNbrChild; ++i) {
    objListUid[i].getElementsByTagName('input')[1].classList.remove("inputError");
    if (objListUid[i].getElementsByTagName('input')[0].value.trim().length > 0) {
      if (objListUid[i].getElementsByTagName('input')[1].value.trim().length == 0
      || /^\d+$/.test(objListUid[i].getElementsByTagName('input')[1].value.trim()) == false) {
        objListUid[i].getElementsByTagName('input')[1].classList.add("inputError");
        bValuesValid = false;
      }

      var objListInp = objListUid[i].getElementsByTagName('input');
      arrTmp = [];
      arrTmp.push(objListInp[0].value);
      arrTmp.push(objListInp[1].value);
      listUid.push(arrTmp);
    }
  }

  if (!bValuesValid)
    $('.ui.modal').transition('bounce');
  else if (listUid.length > 0)
    prepareReq('sk__req', 'proc', 'sk_mod_banu', JSON.stringify(listUid));
}
</script>