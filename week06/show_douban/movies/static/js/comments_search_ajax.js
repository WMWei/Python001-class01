function prev_page(url) {
    var start = parseInt($("#start").val());
    var pagesize = parseInt($("#pagesize").val());
    comments_search(url, start-pagesize, pagesize);
};

function next_page(url) {
    var start = parseInt($("#start").val());
    var pagesize = parseInt($("#pagesize").val());
    comments_search(url, start+pagesize, pagesize);
};

//comments search
function comments_search(url, start=0, pagesize=10) {
    var q_str =  $("#comments-queries").val().replace(" ", "+"); // 获取查询输入框的值
    var data = {
        "start": start,
        "pagesize": pagesize,
        "q": q_str,
    };  // 打包成get请求发送的数据

    $.ajax({
        type: 'get',
        url: url,
        data: data,
        dataType: 'json',
        success: function(ret) {
            var newhtml = ret.page;
            $('#comments-page').html(newhtml);
        },
        error: function(XMLHttpRequest) {
            var _code = XMLHttpRequest.status;
            if (_code == 404) {
                var error_text = '未查询到结果！';
            } else if (_code == 500) {
                var error_text = '请求超时，请稍后重试！'
            } else {
                var error_text = '未知错误...'
            }
            var newhtml = '<div class="media-body">' + error_text + '</div>';
            $('#comments-page').html(newhtml);
        }
    })
}