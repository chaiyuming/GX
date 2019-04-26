//通过一级分类获取二级分类
$(function () {
    var top_tags_select=$('#top_category');
    var sub_tags_select=$('#sub_category');
    top_tags_select.change(function () {
        var top_tag_id=$(this).val();
        if(top_tag_id === '0'){
            sub_tags_select.children('option').remove();
            sub_tags_select.append('<option value="0">- - -  二级分类  - - -</option>');
            return
        }
        $.ajax({
            url:'/cms/sub_by_top/'+top_tag_id+'/',
            type: 'GET',
            dataType: 'json'
        })
            .done(function (res) {
                if (res.errno === '0') {
                    sub_tags_select.children('option').remove();
                    sub_tags_select.append('<option value="0">- - -  二级分类  - - -</option>');
                    res.data.sub_tags.forEach(function (one_tag) {
                        // $.each(res.data.news,function (i,one_news) {
                        // 效果跟上面res.data.news.forEach(function (one_news)一样
                        sub_tags_select.append('<option value=' + one_tag.id + '>' + one_tag.name + '</option>');
                    });
                }
            })
    })

});