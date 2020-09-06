function prev_page(url,) {
    var page_no = parseInt($("#c-page-no").text());
    var page_size = parseInt($("#c-page-size").val());
    comments_search(url, page_no-1, page_size);
    var offset_top = $("#search-str").offset().top;
    $(window).scrollTop(offset_top);

};

function next_page(url,) {
    var page_no = parseInt($("#c-page-no").text());
    var page_size = parseInt($("#c-page-size").val());
    comments_search(url, page_no+1, page_size);
    var offset_top = $("#search-str").offset().top;
    $(window).scrollTop(offset_top);
};

//comments search
function comments_search(url, page_no=1, page_size=10) {
    var q_str =  $("#search-str").val().replace(" ", "+"); // 获取查询输入框的值
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


//sentiments analysis
function sent_analysis(url) {
    var q_str =  $("#search-str").val().replace(" ", "+"); // 获取查询输入框的值
    var data = {
        "q": q_str,
    };  // 打包成get请求发送的数据
    // 用于加载echart的Pie图标
    var myChart = echarts.init(document.getElementById('pie'));

    $.ajax({
        type: 'get',
        url: url,
        data: data,
        dataType: 'json',
        success: function(ret) {
            var newhtml = ret.page;
            var minus = parseInt(ret.params.minus);
            var plus = parseInt(ret.params.plus);
            // 指定图表的配置项和数据
            var option = {
                tooltip: {
                    trigger: 'item',
                    formatter: '{a} <br/>{b}: {c} ({d}%)'
                },
                legend: {
                    orient: 'vertical',
                    left: 10,
                    data: ['正向评价', '负向评价']
                },
                series: [
                    {
                        name: '情感倾向',
                        type: 'pie',
                        radius: ['70%', '90%'],
                        avoidLabelOverlap: false,
                        label: {
                            show: false,
                            position: 'center'
                        },
                        emphasis: {
                            label: {
                                show: true,
                                fontSize: '30',
                                fontWeight: 'bold'
                            }
                        },
                        labelLine: {
                            show: false
                        },
                        data: [
                            {value: plus, name: '正向评价'},
                            {value: minus, name: '负向评价'},
                        ]
                    }
                ]
            };
            // 使用刚指定的配置项和数据显示图表。
            $('#graph-card').html(newhtml);
            myChart.setOption(option);
        },
        error: function(XMLHttpRequest) {
            var _code = XMLHttpRequest.status;
            if (_code == 404) {
                var error_text = '查询出错！';
            } else if (_code == 500) {
                var error_text = '请求超时，请稍后重试！'
            } else {
                var error_text = '未知错误...'
            }
            var newhtml = '<ol class="breadcrumb"><li class="breadcrumb-item">' + error_text + '</li></ol>'
            $('#graph-card').html(newhtml);
        }
    })
}