//富文本编辑器
$(function () {
    //此处UE为html文件中导入ueditor的js文件自带的。
    //window.ue是将ue这个变量变为全局变量
    window.ue = UE.getEditor('editor',{
        initialFrameHeight:400,
        serverUrl:'/ueditor/upload/'
    });
});


//发布新闻内容/编辑新闻内容
$(function () {
   var submitBtn=$('#submit-btn');
    submitBtn.click(function (e) {
        e.preventDefault();
        var news_title=$('#news-title').val();
        if(!news_title){
            message.showError('请输入新闻标题！');
            return
        }
        //新闻内容是从富文本中获取，window.ue.getContent()可获取编辑器html的内容。
        var news_content=window.ue.getContent();
        if(!news_content  || news_content === '<p><br></p>'){
            message.showError('请输入新闻内容！');
            return
        }
        var news_id=$(this).data('news-id');
        var url=news_id ? '/cms/news/'+news_id+'/' : '/cms/news/';
        var data={
            "title":news_title,
            "content":news_content
        };
        $.ajax({
            url:url,
            type:news_id ? 'PUT' : 'POST',
            contentType: "application/json; charset=utf-8",
            data:JSON.stringify(data),
            dataType: "json"
        })
            .done(function (res) {
                if(res.errno === "0"){
                    if(news_id){
                        fAlert.alertSuccess('新闻更新成功',function () {
                            //返回上一个页面
                            window.location.href=document.referrer;
                        })
                    }else {
                        fAlert.alertSuccess('新闻发布成功',function () {
                            window.location.reload();
                        })
                    }
                }else {
                    fAlert.alertErrorToast(res.errmsg);
                }
            })
            .fail(function () {
                message.showError('服务器超时，请重试！');
            })
    });
});

$(function () {
      // get cookie using jQuery
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }

  // Setting the token on the AJAX request
  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
      }
    }
  });

});