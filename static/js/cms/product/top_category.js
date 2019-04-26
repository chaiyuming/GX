//add创建标签
$(function () {
    var addbtn = $('#add-btn');
    addbtn.click(function (e) {
        e.preventDefault()
        fAlert.alertOneInput({
            'title': '添加一级分类！',
            'text': "长度限制在20字以内",
            'placeholder': '请输入产品一级分类',
            'confirmCallback': function (inputValue) {
                if (inputValue === "") {
                    swal.showInputError("标签不能为空！");
                    return false
                }
                var sDataPramas = {
                    "name": inputValue
                };
                $.ajax({
                    url: "/cms/top_category/",
                    type: "POST",
                    data: JSON.stringify(sDataPramas),
                    contentType: "application/json; charset=utf-8",
                    dataType: "json"
                })
                    .done(function (res) {
                        if (res.errno === '0') {
                            fAlert.alertSuccessToast(inputValue + "一级分类创建成功");
                            // swal.close();
                            setTimeout(function () {
                                window.location.reload()
                            }, 800)

                        } else {
                            swal.showInputError(res.errmsg)
                        }
                    })
                    .fail(function () {
                        window.message.showError("服务器超时！")
                    })
            }
        })
    })
});

//delete
$(function () {
    var del_btn = $('.btn-del');
    del_btn.click(function () {
        var _this = this;
        var current_btn = $(this);
        var tag = current_btn.parents('tr');
        var top_tag_id = tag.data('id');
        var tag_name = tag.data('name');
        fAlert.alertConfirm({
            'title': '确定删除' + tag_name + '标签吗？',
            'type': 'error',
            'confirmCallback': function () {
                $.ajax({
                    url: '/cms/top_category/' + top_tag_id + '/',
                    type: "DELETE",
                    dataType: "json"
                })
                    .done(function (res) {
                        if (res.errno === "0") {
                            // window.message.showSuccess('标签删除成功');
                            $(_this).parents('tr').remove();
                            window.location.reload();
                        } else {
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
//edit
$(function () {
    var btn_edit = $('.btn-edit');
    btn_edit.click(function (e) {
        e.preventDefault();
        var _this = $(this);
        var current = $(this);
        var tr = current.parents('tr');
        var top_tag_id = tr.data('id');
        var tag_name = tr.data('name');
        fAlert.alertOneInput({
            'title': '编辑产品一级标签',
            'text': '您正在编辑' + tag_name + '标签',
            'value': tag_name,
            'placeholder': "请输入产品一级标签",
            'confirmCallback': function (inputValue) {
                if (inputValue === tag_name) {
                    swal.showInputError('标签名未发生改变！');
                    return false;
                }
                var sDataParams = {
                    'name': inputValue
                };
                $.ajax({
                    url: '/cms/top_category/' + top_tag_id + '/',
                    data: JSON.stringify(sDataParams),
                    type: 'PUT',
                    dataType: 'json',
                    contentType: "application/json; charset=utf-8"
                })
                    .done(function (res) {
                        if (res.errno === '0') {
                            //知道this标签下tr的祖宗级标签，.find()找到tr标签下的第一个td标签
                            $(_this).parents('tr').find('td:nth-child(1)').text(inputValue);
                            swal.close();
                            window.message.showSuccess('标签修改成功！');
                            setTimeout(function () {
                                window.location.href = '/cms/top_category/';
                            }, 800);
                        } else {
                            swal.showInputError(res.errmsg);
                        }

                    })
                    .fail(function () {
                        window.message.showError('服务器超时！')
                    })
            }
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