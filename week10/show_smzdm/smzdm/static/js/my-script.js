function prev_page(url,) {
    var page_no = parseInt($('#c-page-no').text());
    var page_size = parseInt($('#c-page-size').val());
    comments_search(url, page_no-1, page_size);
    var offset_top = $('#search-str').offset().top;
    $(window).scrollTop(offset_top);

};

function next_page(url,) {
    var page_no = parseInt($('#c-page-no').text());
    var page_size = parseInt($('#c-page-size').val());
    comments_search(url, page_no+1, page_size);
    var offset_top = $('#search-str').offset().top;
    $(window).scrollTop(offset_top);
};

//comments search
function comments_search(url, page_no=1, page_size=10) {
    var q_str =  $('#search-str').val().replace(' ', '+'); // 获取查询输入框的值
    var data = {
        'pageNo': page_no,
        'pageSize': page_size,
        'q': q_str,
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
            var newhtml = '<p class="lead text-gray-800 mb-5">'+ error_text + '</p>'
            $('#comments-page').html(newhtml);
        }
    })
}


function get_table(url) {
    
    // ajax错误处理
    // $.fn.dataTable.ext.errMode = function ( settings, helpPage, message ) { 
    //     console.log(message);
    // };
    // 渲染table
    var table = $('#dataTable').DataTable( {
        // 特性
        // 'scrollY': '200px',
        // 'paging': false,
        'processing': true,
        'lengthMenu': [ [10, 25, 50, -1], [10, 25, 50, "所有"] ],
        'order': [[2, 'desc']],
        'renderer': "bootstrap",
        'language': {
            'paginate': {
                'first': '«',
                'previous': '‹',
                'next': '›',
                'last': '»'
            },
            'aria': {
                'paginate': {
                    'first': 'First',
                    'previous': 'Previous',
                    'next': 'Next',
                    'last': 'Last'
                }
            },
            'infoEmpty': '没有记录可以显示',
            'emptyTable': '没有记录可以显示',
            'infoFiltered': ' - 从 _MAX_ 记录中过滤',
            'info': '第_PAGE_页(共_PAGES_页）',
            'lengthMenu': '显示 _MENU_ 条记录',
            'loadingRecords': '请等待，数据正在加载中......',
            'search': '过滤记录:',
            'searchPlaceholder': '搜索...',
        },
        // 数据
        // 'data': comments,
        // 通过ajax获取数据
        'ajax': {
            'url': url,
            'dataSrc': 'table_data',
            'data': function ( d ) {
                //添加额外的参数传给服务器
                d.timeRange = $('#reportrange span').html();
            },
            'error': function (xhr, error, code)
            {
                console.log(xhr);
                console.log(code);
                var _code = xhr.status;
                if (_code == 404) {
                    var error_text = '未查询到结果！';
                } else if (_code == 500) {
                    var error_text = '请求超时，请稍后重试！'
                } else {
                    var error_text = '未知错误...'
                }
                var newhtml = '<p class="lead text-gray-800 mb-5">'+ error_text + '</p>'
                $('#graph-table').html(newhtml);
            }
        },
        // 单元格格式
        'columns': [
            {
                'data': 'cid',
                'width': '5%',
            },
            {
                'data': 'username',
                'width': '10%',
            },
            {
                'data': 'pub_date',
                'width': '25%',
            },
            {
                'data': 'comment',
                'width': '45%',
            },
            {
                'data': 'sentiments',
                'width': '15%',
            },
        ],
        // 按时间筛选
        // 'dom': "<'row'<'span9'l><'span3'f>r>"+
        //         "t"+
        //         "<'row'<'span6'i><'span6'p>>"  ,
        'dom':  "<'row'<'col-sm-6'l><'col-sm-6'f>>" +
                "<'row'<'col-sm-12'<'#mytoolbox'>>>" +
                "<'row'<'col-sm-12'tr>>" +
                "<'row'<'col-sm-5'i><'col-sm-7'p>>",
        'initComplete': initComplete1,
        
      } );
    
    // 数据加载完毕后的处理
    function initComplete1(settings, json){
        // card
        var card_params = json.card_params;
        // pie
        var pie_labels = ['正向情感', '负向情感'];
        var pie_datas = [card_params.plus, card_params.minus];
        var bg_colors = ['#1cc88a', '#e74a3b'];
        var hbg_colors = ['#17a673', '#e74a3b'];
        var hbord_colors = 'rgba(234, 236, 244, 1)';
        // 渲染汇总数据
        $('#c_count').append(card_params.c_count);
        $('#plus').append(card_params.plus);
        $('#minus').append(card_params.minus);
        $('#sent_avg').append(card_params.sent_avg);
        // 渲染饼图
        get_pie(pie_labels, pie_datas, bg_colors, hbg_colors, hbord_colors);
        // ---
        // 绘制时间选择框
        get_time_tag();
        //选择时间后触发重新加载的方法
        $("#reportrange").on('apply.daterangepicker',function(){
            //当选择时间后，触发dt的重新加载数据的方法
            table.ajax.reload();
            //获取dt请求参数
            var args = table.ajax.params();
            console.log("额外传到后台的参数值time_range为："+args.timeRange);
        });
    
        // function getParam(url) {
        //     var data = decodeURI(url).split("?")[1];
        //     var param = {};
        //     var strs = data.split("&");
    
        //     for(var i = 0; i<strs.length; i++){
        //         param[strs[i].split("=")[0]] = strs[i].split("=")[1];
        //     }
        //     return param;
        // }
    };
}

// 绘制时间选择框
function get_time_tag(){
    var dataPlugin =
        '<div id="reportrange" class="pull-left dateRange"> '+
        '日期：<i class="glyphicon glyphicon-calendar fa fa-calendar"></i> '+
        '<span id="searchDateRange"></span>  '+
        '<b class="caret"></b></div> ';
    $('#mytoolbox').append(dataPlugin);
    //时间插件
    //$('#reportrange span').html(moment().subtract('hours', 1).format('YYYY-MM-DD HH:mm:ss') + ' - ' + moment().format('YYYY-MM-DD HH:mm:ss'));

    $('#reportrange').daterangepicker(
        {
            // startDate: moment().startOf('day'),
            //endDate: moment(),
            //minDate: '01/01/2000',    //最小时间
            maxDate : moment(), //最大时间
            dateLimit : {
                days : 30
            }, //起止时间的最大间隔
            showDropdowns : true,
            showWeekNumbers : false, //是否显示第几周
            timePicker : true, //是否显示小时和分钟
            timePickerIncrement : 60, //时间的增量，单位为分钟
            timePicker12Hour : false, //是否使用12小时制来显示时间
            ranges : {
                '最近1小时': [moment().subtract('hours',1), moment()],
                '最近12小时': [moment().subtract('hours',12), moment()],
                '今日': [moment().startOf('day'), moment()],
                '昨日': [moment().subtract('days', 1).startOf('day'), moment().subtract('days', 1).endOf('day')],
                '最近7日': [moment().subtract('days', 6), moment()],
                '最近30日': [moment().subtract('days', 29), moment()]
            },
            opens : 'right', //日期选择框的弹出位置
            buttonClasses : [ 'btn btn-default' ],
            applyClass : 'btn-small btn-primary blue',
            cancelClass : 'btn-small',
            format : 'YYYY-MM-DD HH:mm:ss', //控件中from和to 显示的日期格式
            separator : ' to ',
            locale : {
                applyLabel : '确定',
                cancelLabel : '取消',
                fromLabel : '起始时间',
                toLabel : '结束时间',
                customRangeLabel : '自定义',
                daysOfWeek : [ '日', '一', '二', '三', '四', '五', '六' ],
                monthNames : [ '一月', '二月', '三月', '四月', '五月', '六月',
                    '七月', '八月', '九月', '十月', '十一月', '十二月' ],
                firstDay : 1
            }
        }, 
        function(start, end, label) {//格式化日期显示框
            $('#reportrange span').html(start.format('YYYY-MM-DD HH:mm:ss') + ' - ' + end.format('YYYY-MM-DD HH:mm:ss'));
        }
    );

    //设置日期菜单被选项  --开始--
    var dateOption ;
    if("${riqi}"=='day') {
        dateOption = "今日";
    }else if("${riqi}"=='yday') {
        dateOption = "昨日";
    }else if("${riqi}"=='week'){
        dateOption ="最近7日";
    }else if("${riqi}"=='month'){
        dateOption ="最近30日";
    }else if("${riqi}"=='year'){
        dateOption ="最近一年";
    }else{
        dateOption = "自定义";
    }
    $(".daterangepicker").find("li").each(function (){
        if($(this).hasClass("active")){
            $(this).removeClass("active");
        }
        if(dateOption==$(this).html()){
            $(this).addClass("active");
        }
    });
    //设置日期菜单被选项  --结束--
}

// 渲染 pie
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

// Pie Chart Example
// chartjs
function get_pie(labels, datas, bg_colors, hbg_colors, hbord_colors) {
    var ctx = document.getElementById('myPieChart');
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
        responsive: true,
        maintainAspectRatio: false,
        tooltips: {
            backgroundColor: 'rgb(255,255,255)',
            bodyFontColor: '#858796',
            borderColor: '#dddfeb',
            borderWidth: 1,
            xPadding: 15,
            yPadding: 15,
            displayColors: false,
            caretPadding: 10,
        },
        legend: {
            display: true,
            position: 'bottom',
            // align: 'start',
            //onClick: ,
            // onHover:,
        },
        cutoutPercentage: 80,
    },
    });
}
