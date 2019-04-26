$(function () {
    var PubBtn=$('#submit-btn');
    PubBtn.click(function () {
        var brand=$('#product-brand').val();
        if(!brand){
            message.showError('请输入产品品牌！');
            return
        }
        var version=$('#product-version').val();
        if(!version){
            message.showError('请输入产品型号！');
            return
        }
        var describe=$('#product-describe').val();
        if(!describe){
            message.showError('请输入产品型号！');
            return
        }
        var top_tag_id=$('#top_category').val();
        if(!top_tag_id || top_tag_id === '0'){
            message.showError('请选择产品一级标签！');
            return
        }
        var sub_tag_id=$('#sub_category').val();
        if(!sub_tag_id || sub_tag_id === '0'){
            message.showError('请选择产品一级标签！');
            return
        }
        var thumbnail=$('#product-thumbnail').val();
        if(!thumbnail){
            message.showError('请输入产品缩略图！');
            return
        }
        var product_id=$(this).data('product-id');
        var url =product_id ? '/cms/product/'+product_id+'/' : '/cms/add_product/'
        var data={
            'thumbnail':thumbnail,
            'top_tag_id':top_tag_id,
            'sub_tag_id':sub_tag_id,
            'brand':brand,
            'version':version,
            'describe':describe
        };
        $.ajax({
            url:url,
            data:JSON.stringify(data),
            contentType: "application/json; charset=utf-8",
            type:product_id ? 'PUT' : 'POST',
            dataType: "json"
        })
            .done(function (res) {
                if(res.errno==='0'){
                    if(product_id){
                        fAlert.alertSuccess('产品更新成功',function () {
                            window.location.href=document.referrer;
                        })
                    }else {
                        fAlert.alertSuccess('产品发布成功',function () {
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


    })

});



//图片上传到FASTDFS服务器
$(function () {
 var $upload_to_server = $("#upload_news_to_fds");
  //一个元素的值改变的时候将触发change事件。此事件仅限用于<input>元素，<textarea>和<select>元素。
    // 对于下拉选择框，复选框和单选按钮，当用户用鼠标作出选择，该事件立即触发，但对于其他类型的input元素，该事件触发将推迟，直到元素失去焦点才会触点。
  $upload_to_server.change(function () {
      //this表示当前的按钮，.files[0]表示当前选中的文件。
    var file = this.files[0];   // 获取文件
    var oFormData = new FormData();  // 创建一个 FormData
    oFormData.append("image_file", file); // 把文件添加进去
    // 发送请求
    $.ajax({
      url: "/cms/product/images/",
      method: "POST",
      data: oFormData,
      processData: false,   // 定义文件的传输
      contentType: false
    })
      .done(function (res) {
        if (res.errno === "0") {
          // 更新标签成功
          message.showSuccess("图片上传成功");
          var sImageUrl = res["data"]["image_url"];
          // console.log(thumbnailUrl);
          var image_url=$('#product-thumbnail');
          image_url.val('');
          image_url.val(sImageUrl);
        } else {
          message.showError(res.errmsg)
        }
      })
      .fail(function () {
        message.showError('服务器超时，请重试！');
      });

  });
});

//上传到七牛云服务器
$(function () {
      // ================== 上传至七牛（云存储平台） ================
  var $progressBar = $(".progress-bar");
  var image_url=$('#product-thumbnail');
  QINIU.upload({
    "domain": "http://www.gongxietech.com/",  // 七牛空间域名
    // 后台返回 token的地址 (后台返回的 url 地址) 不可能成功
    "uptoken_url": "/cms/token/",
    // 按钮
    "browse_btn": "upload-btn",
    "success": function (up, file, info) {
      var domain = up.getOption('domain');
      var res = JSON.parse(info);
      var filePath = domain + res.key;
      console.log(filePath);  // 打印文件路径
      image_url.val('');
      image_url.val(filePath);
    },
    "error": function (up, err, errTip) {
      console.log(up);
      console.log(err);
      console.log(errTip);
      // console.log('error');
      message.showError(errTip);
    },
    "progress": function (up, file) {
      var percent = file.percent;
      $progressBar.parent().css("display", 'block');
      $progressBar.css("width", percent + '%');
      $progressBar.text(parseInt(percent) + '%');
    },
    "complete": function () {
      $progressBar.parent().css("display", 'none');
      $progressBar.css("width", '0%');
      $progressBar.text('0%');
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