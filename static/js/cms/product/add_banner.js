//add banner
$(function () {
    var savebtn=$('#save-btn');
    savebtn.click(function () {
        var image_url=$(".banner-image").attr('src');
        var priority=$("#priority").val();
        var link_to=$('#link_to').val();
        if(image_url==='/static/images/banner.png'){
            window.message.showInfo('轮播图不能为默认图片');
            return
        }
        if(priority !== '0' && image_url && link_to){
            var data={
                'image_url':image_url,
                'priority':priority,
                'link_to':link_to
            };
            $.ajax({
                url:'/cms/add/banner/',
                data:JSON.stringify(data),
                dataType:'json',
                type:'POST',
                contentType:'application/json;charset=utf-8'
            })
                .done(function (res) {
                    if(res.errno==='0'){
                        window.message.showSuccess('轮播图创建成功！');
                        setTimeout(function () {
                            window.location.href='/cms/banners/'
                        },1000)
                    }else {
                        window.message.showError(res.errmsg)
                    }
                })
                .fail(function () {
                    window.message.showError('服务器超时，请重试！')
                })
        }else {
            window.message.showError('优先级和跳转链接不能为空！')
        }
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