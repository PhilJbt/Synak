<table class="ui selectable celled table very compact collapsing four column %TABLE_COLOR%">
  <thead>
    <tr><th>VARIABLE</th>
    <th>EXPECTED VALUE</th>
    <th>CURRENT VALUE</th>
    <th>STATUS</th>
  </tr></thead>
  <tbody>
    %VARS_LIST%
  </tbody>
  <tfoot>
    <tr>
    <th>
      <i id="popnfo_sttdeb" class="info help icon link"></i>
      <div class="ui flowing popup top left transition visible animating scale out">
        <p>Please read the <a target="_blank" href="https://github.com/PhilJbt/Synak/wiki/Web-Panel">Synak Wiki</a> to learn how to change these values temporarily or permanently.</p>
      </div>
    </th>
    <th></th>
    <th></th>
    <th>%ERR_COUNT%</th>
    </tr>
  </tfoot>
</table>
<script>
function template_init() {
  $('#popnfo_sttdeb').popup({hoverable  : true});
}
</script>