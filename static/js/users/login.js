$(function () {
    var loginbtn = $('.form-contain');
    loginbtn.submit(function (e) {
        e.preventDefault();
        var sUserAccount = $("input[name='telephone']").val();
        var password = $("input[name='password']").val();
        if (sUserAccount === '') {
            window.message.showError('用户账号不能为空！');
            return
        }
        if(!(/^\w{5,20}$/).test(sUserAccount) || !(/^1[3456789]\d{9}$/).test(sUserAccount)){
        // if (!(/^\w{5,20}$/).test(sUserAccount) || !(/^\w{5,20}$/).test(sUserAccount)) {
            window.message.showError('请输入合法的用户账号：5-20个字符的用户名或者11位手机号');
            return
        }
        if (!password) {
            window.message.showError('密码不能为空！');
            return
        }
        if (password.length < 6 || password.length > 20) {
            window.message.showError('密码的长度需在6～20位以内');
            return
        }
        var data = {
            'user_account': sUserAccount,
            'password': password
        };
        $.ajax({
            url: '/users/login/',
            type: 'POST',
            data: JSON.stringify(data),
            contentType: "application/json; charset=utf-8",
            dataType: "json"
        })
            .done(function (res) {
                if (res.errno === "0") {
                    window.message.showSuccess("恭喜您！登陆成功！");
                    setTimeout(function () {
                        window.location.href = '/cms/'
                    }, 1000)
                } else {
                    window.message.showError(res.errmsg);
                }
            })
            .fail(function () {
                window.message.showError('服务器超时，请重试！')
            });

    });

    // get cookie using jQuery
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
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
