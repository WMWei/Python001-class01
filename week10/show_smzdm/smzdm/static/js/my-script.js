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


function get_analysis(url) {
    // var q_str =  $("#search-str").val().replace(" ", "+"); // 获取查询输入框的值
    // var data = {
    //     "q": q_str,
    // };  // 打包成get请求发送的数据

    $.ajax({
        type: 'get',
        url: url,
        //data: data,
        dataType: 'json',
        success: function(ret) {
            // card
            var card_params = ret.card_params;
            // pie
            var pie_labels = ['正向情感', '负向情感'];
            var pie_datas = [card_params.plus, card_params.minus];
            var bg_colors = ['#1cc88a', '#e74a3b'];
            var hbg_colors = ['#17a673', '#e74a3b'];
            var hbord_colors = "rgba(234, 236, 244, 1)";
            // table
            var table_data = ret.table_data;
            // 渲染表格
            // 渲染汇总数据
            $('#c_count').append(card_params.c_count);
            $('#plus').append(card_params.plus);
            $('#minus').append(card_params.minus);
            $('#sent_avg').append(card_params.sent_avg);
            get_pie(pie_labels, pie_datas, bg_colors, hbg_colors, hbord_colors);
            get_table(table_data);

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
            var newhtml = '<p class="lead text-gray-800 mb-5">'+ error_text + '</p>'
            $('#graph-card').html(newhtml);
            //$('#graph-pie').html(newhtml);
            $('#graph-table').html(newhtml);
        }
    })
}

// 渲染table


function get_table(comments) {
    // 渲染table
    $('#dataTable').DataTable( {
        // 特性
        "processing": true,
        // 数据
        "data": comments,
        // 单元格格式
        "columns": [
            {
                "data": "cid",
                "width": "5%",
            },
            {
                "data": "username",
                "width": "10%",
            },
            {
                "data": "pub_date",
                "width": "25%",
            },
            {
                "data": "comment",
                "width": "65%",
            },
            {
                "data": "sentiments",
                "width": "5%",
            },
        ]
      } );
}

// 渲染 pie
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

// Pie Chart Example
function get_pie(labels, datas, bg_colors, hbg_colors, hbord_colors) {
    var ctx = document.getElementById("myPieChart");
    var myPieChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: labels,
        datasets: [{
        data: datas,
        backgroundColor: bg_colors,
        hoverBackgroundColor: hbg_colors,
        hoverBorderColor: hbord_colors,
        }],
    },
    options: {
        maintainAspectRatio: false,
        tooltips: {
        backgroundColor: "rgb(255,255,255)",
        bodyFontColor: "#858796",
        borderColor: '#dddfeb',
        borderWidth: 1,
        xPadding: 15,
        yPadding: 15,
        displayColors: false,
        caretPadding: 10,
        },
        legend: {
        display: false
        },
        cutoutPercentage: 80,
    },
    });
}
