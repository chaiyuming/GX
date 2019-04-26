$(function () {
	$(".left_nav ul li .t").click(function(){
		$(this).toggleClass("hover");
		var Txt=$(this).next(".txt");
		Txt.slideToggle().parent().siblings().children(".txt").hide(500);
	});
});
$(function () {
    var url=location.search;  //获取url中"?"符后的字串
     if (url.indexOf("?") != -1) { // 判断是否有参数
         var str = url.substr(1); //从第一个字符开始 因为第0个是?号 获取所有除问号的所有符串
         var strs = str.split("=");   //用等号进行分隔 （因为知道只有一个参数 所以直接用等号进分隔 如果有多个参数 要用&号分隔 再用等号进行分隔）
         var top_tag_id = strs[1];
         var LiBtn=$(".left_nav ul li");
         for(let i=0;i<LiBtn.length;i++){
             var T=LiBtn.eq(i).children('.t');
             var Txt=T.next('.txt');
             var T_btn=T.data('tag-id');
             if(top_tag_id == T_btn){
                 Txt.css('display','block');
             }
         }
     }
});
$(function () {
    var url=location.search;  //获取url中"?"符后的字串
     if (url.indexOf("?") != -1) { // 判断是否有参数
         var str = url.substr(1); //从第一个字符开始 因为第0个是?号 获取所有除问号的所有符串
         var _str = str.split("&");
         var sub =_str[0];
         var strs = sub.split("=");   //用等号进行分隔 （因为知道只有一个参数 所以直接用等号进分隔 如果有多个参数 要用&号分隔 再用等号进行分隔）
         var top_tag_id = strs[1];
         var LiBtn=$(".left_nav ul li");
         for(let i=0;i<LiBtn.length;i++){
             var T=LiBtn.eq(i).children('.t');
             var Txt=T.next('.txt');
             var T_btn=T.data('tag-id');
             if(top_tag_id == T_btn){
                 Txt.css('display','block');
             }
         }
     }
});


