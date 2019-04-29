//banner image upload to fasefdfs
$(function () {
    var imageselect=$('input[name="banner-image-select"]');
    var imagebtn=$('.banner-image');
    imagebtn.click(function () {
        $(this).prev().click()
    });
    imageselect.change(function () {
       var _this=this;
       var file= this.files[0];
       var formData=new FormData();
        formData.append('image_file',file);
        $.ajax({
            url:"/cms/product/images/",
            method: "POST",
            data: formData,
            processData: false,   // 定义文件的传输
            contentType: false
        })
            .done(function (res) {
                if (res.errno==='0'){
                    var sImageUrl = res["data"]["image_url"];
                    $(_this).next().attr('src',sImageUrl)
                }else {
                     message.showError(res.errmsg)
                }
            })
            .fail(function () {
                message.showError('服务器超时，请重试！');
            })
    })
});

