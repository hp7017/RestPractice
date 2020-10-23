$(".download-link").click(function(){
    $('#overlay-spinner').attr('style',  'display: block')
    pat = window.location.href
    $(".overlay").show()
    $.get("/book-clicked", {
        'id': $(this).attr('hr'),
        'name': $(this).attr('title'),
        'path': pat
    }, function(data){
        window.location.href = data;
        $('#overlay-spinner').attr('style',  'display: none')
    })
})