function prev_page(url,) {
    var page_no = parseInt($("#c-page-no").text());
    var page_size = parseInt($("#c-page-size").val());
    comments_search(url, page_no-1, page_size);
};

function next_page(url,) {
    var page_no = parseInt($("#c-page-no").text());
    var page_size = parseInt($("#c-page-size").val());
    comments_search(url, page_no+1, page_size);
};

//comments search
function comments_search(url, page_no=1, page_size=10) {
    var q_str =  $("#comments-queries").val().replace(" ", "+"); // 获取查询输入框的值
    var data = {
        "pageNo": page_no,
        "pageSize": page_size,
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
            var newhtml = '<ol class="breadcrumb"><li class="breadcrumb-item">' + error_text + '</li></ol>'
            $('#comments-page').html(newhtml);
        }
    })
}