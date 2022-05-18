<div class="ui segments">
  <div class="ui segment">
    <p>Web Panel Listening Port</p>
  </div>
  <div class="ui secondary segment">
    <div class="ui sub header"></div>
    <div class="ui form">
      <div class="inline field">
        <input id="in_port_webpanel" type="text" value="%portWP%" placeholder="45318" min="40000" max="65535" onkeypress="return event.charCode>=48 && event.charCode<=57"/>
        <div id="popup_port_webpanel" class="ui left pointing red basic label popuperr">
          Null
        </div>
      </div>
    </div>
  </div>
</div>
<div class="ui segments">
  <div class="ui segment">
    <p>Web Panel Listening Port</p>
  </div>
  <div class="ui secondary segment">
    <div class="ui form">
      <div class="inline field">
        <input id="in_port_players" type="text" value="%portPL%" placeholder="45350" min="40000" max="65535" onkeypress="return event.charCode>=48 && event.charCode<=57"/>
        <div id="popup_port_players" class="ui left pointing red basic label popuperr">
          Null
        </div>
      </div>
    </div>
  </div>
</div>
<script type="text/javascript">
function showErrPop(_node, _mess) {
  _node.style.opacity = 1;
  _node.innerHTML = _mess;
}
function hideErrPop(_node) {
  _node.style.opacity = 0;
}
</script>