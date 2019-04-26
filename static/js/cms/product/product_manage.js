//delete
$(function () {
   var del_btn=$('.btn-del');
   del_btn.click(function () {
       var _this=this;
       var current_btn=$(this);
       var $tr= current_btn.parents('tr');
       var product_id=$tr.data('id');
       var product_version=$tr.data('name');
       fAlert.alertConfirm({
           'title':'确定删除'+product_version+'型号的产品吗？',
           'type':'error',
           'confirmCallback':function () {
               $.ajax({
                   url:'/cms/product/'+product_id+'/',
                   //请求方式
                   type:"DELETE",
                   dataType:"json"
               })
                   .done(function (res) {
                       if(res.errno==="0"){
                           window.message.showSuccess('产品删除成功');
                           $(_this).parents('tr').remove();
                           setTimeout(function () {
                               window.location.reload();
                           },1000)

                       }else {
                           swal.showInputError(res.errmsg)
                       }
                   })
                   .fail(function () {
                       window.message.showError('服务器超时，请重试！');
                   });
           }
       });
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