//add banner image
$(function () {
    var  $bannerAddBtn = $("#banner-add-btn");  // 添加轮播图按钮
    var bannerlist=$(".banner-list");
    $bannerAddBtn.click(function () {
        var length=bannerlist.find('li').length;
        if(length >= 6){
            $bannerAddBtn.addClass('disabled');
            window.message.showError('最多只能添加6张图')
        }else {
            window.location.href = '/cms/add/banner/';
        }
    })
});
//delete
$(function () {
    var closebtn=$('.close-btn');
    closebtn.click(function () {
        var _this=this;
        var current=$(this);
        var banner_id=current.parents('li').data('banner-id');
        fAlert.alertConfirm({
            'title': '确定删除这篇新闻吗',
            'text': '删除之后，将无法恢复',
            'type': "warning",
            'confirmCallback':function () {
                $.ajax({
                    url: '/cms/banner/' + banner_id + '/',
                    type: 'DELETE',
                    dataType: 'json'
                })
                    .done(function (res) {
                        if (res.errno === '0') {
                            $(_this).parents('li').remove();
                            window.message.showSuccess('轮播图删除成功！');
                            setTimeout(function () {
                                window.location.href='/cms/banners/'
                            }, 1000);
                        }else {
                            swal.showInputError(res.errmsg)
                        }
                    })
                    .fail(function () {
                        message.showError('服务器超时，请重试！');
                    })
            }
        })
    })

});

//edit
$(function () {
    var updatebtn=$('.update-btn');
    updatebtn.click(function (e) {
        e.preventDefault();
        var libtn=$(this).parents('li');
        var image_url= libtn.find('.banner-image').attr('src');
        var priority=libtn.find('#priority').val();
        var link_to=libtn.find('#link_to').val();
        var banner_id=libtn.data('banner-id');

        //更新之前的数据
        var $image_url=$(this).data('image-utl');
        var $priority=$(this).data('priority');
        var $link_to=$(this).data('link_to');

        if(!image_url){
             message.showError('轮播图url为空');
             return
        }
        if(!link_to){
             message.showError('跳转链接不能为空');
             return
        }
        if(!priority.trim()){
             message.showError('优先级不能为空');
             return
        }
        if(image_url===$image_url && link_to===$link_to && priority == $priority){
            message.showError('未修改任何值');
            return
        }
        var data={
            'priority':priority,
            'image_url':image_url,
            'banner_id':banner_id,
            'link_to':link_to
        };
        $.ajax({
            url:'/cms/banner/'+banner_id+'/',
            data:JSON.stringify(data),
            type:'PUT',
            dataType:'json',
            contentType: "application/json; charset=utf-8"
        })
            .done(function (res) {
                if(res.errno==='0'){
                    message.showSuccess('更新成功');
                     setTimeout(function () {
                         window.location.href='/cms/banners/'
                     },1000)
                }else {
                    message.showError(res.errmsg)
                }

            })
            .fail(function () {
                message.showError('服务器超时，请重试！')
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