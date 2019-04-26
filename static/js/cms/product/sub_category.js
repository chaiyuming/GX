//delete
$(function () {
    var del_btn = $('.btn-del');
    del_btn.click(function () {
        var _this = this;
        var current_btn = $(this);
        var tag = current_btn.parents('tr');
        var sub_tag_id = tag.data('id');
        var tag_name = tag.data('name');
        console.log('0000000000');
        fAlert.alertConfirm({
            'title': '确定删除' + tag_name + '标签吗？',
            'type': 'error',
            'confirmCallback': function () {
                $.ajax({
                    url: '/cms/sub_category/' + sub_tag_id + '/',
                    type: "DELETE",
                    dataType: "json"
                })
                    .done(function (res) {
                        console.log('111111111111');
                        if (res.errno === "0") {
                            console.log('222222222222');
                            window.message.showSuccess('标签删除成功');
                            $(_this).parents('tr').remove();
                            setTimeout(function () {
                                window.location.reload();
                            },1000);

                        } else {
                            console.log('333333333333');
                            window.message.showError(res.errmsg);
                        }
                    })
                    .fail(function () {
                        console.log('44444444444');
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