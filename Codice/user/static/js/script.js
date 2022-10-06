$('#test1').DataTable({});
$('#test2').DataTable({});
$('#test3').DataTable({});
$(".card").click(function () {
  $(this).find("form").submit();
});

$('#test1').click( function() {
  $('#formtest1').submit();
});
$('#test2').click( function() {
  $('#formtest2').submit();
});
$('#test3').click( function() {
  $('#formtest3').submit();
});