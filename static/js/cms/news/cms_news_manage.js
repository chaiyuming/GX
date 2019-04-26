//时间选择器代码
$(function () {
    var options = {
        // 自动关闭
        autoclose: true,
        // 日期格式
        format: 'yyyy/mm/dd',
        // 选择语言为中文
        language: 'zh-CN',
        // 优化样式
        showButtonPanel: true,
        // 高亮今天
        todayHighlight: true,
        // 是否在周行的左侧显示周数
        calendarWeeks: true,
        // 清除
        clearBtn: true,
        // 0 ~11  网站上线的时候
        startDate: new Date(2018, 10, 1),
        // 今天
        endDate: new Date()
    };
    //调用.datepivker({}),就可以实现时间选择器
    $("input[name=start]").datepicker(options);
    $("input[name=end]").datepicker(options);
});

//delete
$(function () {
    var delete_news_btn = $('.delete-news-btn');
    delete_news_btn.click(function () {
        var _this = this;
        var current = $(this);
        var news_id = current.data('news-id');
        fAlert.alertConfirm({
            'title': '确定删除这篇新闻吗',
            'text': '删除之后，将无法恢复',
            'type': "warning",
            'confirmCallback': function () {
                $.ajax({
                    url: '/cms/news/' + news_id + '/',
                    type:'DELETE',
                    dataType:'JSON'
                })
                    .done(function (res) {
                        if (res.errno === '0') {
                            $(_this).parents('tr').remove();
                            window.message.showSuccess('新闻删除成功！');
                            setTimeout(function () {
                                window.location.reload();
                            }, 1000);
                        } else {
                            swal.showInputError(res.errmsg);
                        }
                    })
                    .fail(function () {
                        message.showError('服务器超时，请重试！');
                    });
            }
        })
    })
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