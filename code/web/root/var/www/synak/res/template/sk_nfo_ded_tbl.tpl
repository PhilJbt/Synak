<div class="ui center aligned segment basic secondary">
  %STATS_1%
</div>
<div class="ui center aligned segment basic tertiary">
  %STATS_2%
</div>
<table class="ui selectable celled table very compact  %TABLE_COLOR%">
  <thead>
    <tr>
      <th>STATUS</th>
      <th>VARIABLE</th>
      <th>CURRENT VALUE</th>
      <th>EXPECTED VALUE</th>
    </tr>
  </thead>
  <tbody>
    %VARS_LIST%
  </tbody>
  <tfoot>
    <tr>
    <th>
      <i id="popnfo_sttdeb" class="info help icon link"></i>
      <div class="ui flowing popup">
        <p>These are only optional optimizations, and are not mandatory. In addition, your dedicated server could not correspond to what is usually done, making this configuration obsolete.<br/>Please read the <a target="_blank" href="https://github.com/PhilJbt/Synak/wiki/Web-Panel">Synak Wiki</a> to know how to change these values temporarily or permanently.<br/><b>TL;DR</b>: Don't try if you don't know what you are doing.</p>
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
  $('#popnfo_sttdeb').popup({hoverable : true});
  $('.sk_tbl_pop').popup();
}
</script>