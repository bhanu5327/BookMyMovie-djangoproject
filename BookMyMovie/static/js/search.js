$('#suggestion').keyup(function () {
    var query;
    query=$(this).val();
    $.get('/search/',{suggestion:query},function (data) {
        $('#searchresult').html(data);
    });
});

$('#options').keyup(function () {
    var query;
    query=$(this).val();
    $.get('/search/',{suggestion:query},function (data) {
        $('#searchresult').html(data);
    });
});
