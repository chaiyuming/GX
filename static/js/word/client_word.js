$(function () {
    var submitBtn = $('#submit_id');
    submitBtn.click(function (e) {
        e.preventDefault();
        var username = $('#username').val();
        if (!username) {
            window.alert('请输入姓名^_^');
            username.focus();
            return
        }
        var telephone = $('#telephone').val();
        if (telephone === '') {
            window.alert("手机号码不能为空^_^");
            // document.form1.telephone.focus();
            telephone.focus();
            return
        }
        if (!(/^1[3456789]\d{9}$/).test(telephone)) {
            window.alert("请输入正确的号码^_^");
            return
        }
        var content = $('#content').val();
        if (!content) {
            window.alert("请输入内容^_^");
            // document.form1.telephone.focus();
            content.focus();
            return
        }
        var email = $('#email').val();
        if (email.length > 0 && email.indexOf('@') === -1 | email.indexOf('.') === -1 | email.indexOf('com') === -1) {
            window.alert("请输入内容^_^");
            // document.form1.telephone.focus();
            email.focus();
            return
        }
        var data = {
            'telephone': telephone,
            'username': username,
            'content': content,
            'email': email
        };
        $.ajax({
            url: '/client/words/',
            type: 'POST',
            data: JSON.stringify(data),
            contentType: "application/json; charset=utf-8",
            dataType: "json"
        })
            .done(function (res) {
                if (res.errno === '0') {
                    window.alert('留言提交成功^_^,稍后将会有工作人员与您联系');
                    window.location.reload();
                } else {
                    window.alert(res.errmsg);
                }
            })
            .fail(function () {
               window.alert('服务器超时，请重试！');
            });
    });
});


$(function () {
    // get cookie using jQuery
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            let cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                let cookie = jQuery.trim(cookies[i]);
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