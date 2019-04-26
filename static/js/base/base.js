$(function () {
    var Libox=$('.nav-menu .first_menu');
    for(let i=0;i<Libox.length;i++){
            Libox.eq(i).hover(function () {
                var index=$(this);
                Ulbox=index.children(".nav_second_menu");
                Ulbox.css('display','block');
                index.css('background-color','#6699CC');
                var Ul_libox=$('.nav_second_menu .nav_sec_det');
                Ul_libox.hover(function () {
                    var j =$(this);
                    j.css('background-color','#336699');
                },function () {
                    var j =$(this);
                    j.css('background-color','#6699CC');
                });
             },function () {
                var index=$(this);
                Ulbox=index.children(".nav_second_menu");
                Ulbox.css('display','none');
                index.css('background-color','#336699');
            })
        }
});

$(function () {
    var url=window.location.href;
    var protocol=window.location.protocol;
    var host=window.location.host;
    var domain=protocol+'//'+host;
    var path=url.replace(domain,'');
    var menulis=$('.nav-menu .first_menu');
    for(var index=0;index<menulis.length;index++){
        var li=$(menulis[index]);
        var a =li.children('a');
        var href=a.attr('href');
        if (href===path){
            li.addClass('active');
        }
    }
});
