
//add/edit
$(function () {
    var addBtn = $(".submit-btn");
    addBtn.click(function (e) {
        e.preventDefault();
        var parent_id=$('#first_category').val();
        if(!parent_id ||parent_id === '0'){
            window.message.showInfo('请先选择一级分类！');
            return
        }
        var sub_tag_name=$('#sub_category').val();
        if(!sub_tag_name){
            window.message.showInfo('请输入产品二级分类！');
            return
        }
        var data={
            'sub_tag_name':sub_tag_name,
            'parent_id':parent_id
        };
        var sub_tag_id=$(this).data('type-id');
        var url=sub_tag_id ? '/cms/sub_category/'+sub_tag_id+'/' :'/cms/add_sub_category/';
        $.ajax({
            url:url,
            data:JSON.stringify(data),
            contentType: "application/json; charset=utf-8",
            type:sub_tag_id ? 'PUT' : 'POST',
            dataType: 'json'
        })
            .done(function (res) {
                if(res.errno==='0'){
                    if(sub_tag_id){
                        fAlert.alertSuccess('二级分类更新成功!',function () {
                            window.location.href=document.referrer;
                        })
                    }else {
                        fAlert.alertSuccess('二级分类创建成功!',function () {
                            window.location.reload();
                        })

                    }
                }else {
                    window.message.showError(res.errmsg)
                }
            })
            .fail(function () {
                window.message.showError("服务器超时！")
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