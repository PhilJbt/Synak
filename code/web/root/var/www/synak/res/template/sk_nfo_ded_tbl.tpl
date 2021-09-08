<div class="ui center aligned segment basic secondary">
  %STATS_1%
</div>
<div class="ui center aligned segment basic tertiary">
  %STATS_2%
</div>
<table class="ui selectable celled table very compact %TABLE_COLOR%">
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
    <th></th>
    <th></th>
    <th></th>
    <th>
      <a class="ui labeled button" tabindex="0" href="https://github.com/PhilJbt/Synak/blob/main/wiki/wp/wp_optimization.md" target="_blank">
        <div class="ui yellow button">
          <i class="lightbulb icon"></i> %ERR_COUNT%
        </div>
        <div class="ui basic yellow left pointing label">
          Read more about optimizations
        </div>
      </a>
    </th>
    </tr>
  </tfoot>
</table>
<script>
function template_init() {
  $('.sk_tbl_pop').popup();
}
</script>