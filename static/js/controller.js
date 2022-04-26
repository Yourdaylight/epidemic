

function get_c1_data() {
    $.ajax({
        url: "/c1?region=" + sessionStorage.getItem("region"),
        timeout: 10000,
        success: function (data) {
            $(".num h1").eq(0).text(data.dignose)
            $(".num h1").eq(1).text(data.heal)
            $(".num h1").eq(2).text(data.dead)
            $(".num h1").eq(3).text(data.newly_add)
            if (sessionStorage.getItem("region") === "china") {
                $(".txt").eq(4).html(`<h2 style="color: gold">${data.imported_case}<br><p style="color: white">境外输入</p></h2>`)
                $(".txt").eq(5).html(`<h2 style="color: gold">${data.no_infect}<br><p style="color: white">无症状感染</p></h2>`)
            }
            else {
                $(".txt").eq(4).html("")
                $(".txt").eq(5).html("")
            }
        },
        error: function (xhr, type, errorThrown) {

        }
    })
}

function get_c2_data() {
    let region = sessionStorage.getItem("region")

    $.ajax({
        url: "/c2?region=" + region,
        timeout: 10000,
        success: function (data) {
            //document.getElementById("c2").innerHTML=""
            // ec_center.restore()
            // ec_center=echarts.init(document.getElementById("c2"),"dark")
            if (region === "china") {
                china_map_option.series[0].data = data.data
                ec_center.clear()
                ec_center.setOption(china_map_option)
            } else {
                world_map_option.series[0].data = data.data
                ec_center.clear()
                ec_center.setOption(world_map_option)
            }
        },
        error: function (xhr, type, errorThrown) {

        }
    })
}

function get_l1_data() {
    $.ajax({
        url: "/l1?region=" + sessionStorage.getItem("region"),
        timeout: 10000,
        success: function (data) {
            ec_left1_option.xAxis.data = data.days
            ec_left1_option.series[0].data = data.dignose
            ec_left1_option.series[1].data = data.heal
            ec_left1_option.series[2].data = data.dead
            ec_left1_option.title.text = sessionStorage.getItem("region")==="china"?"全国累计趋势":"全球累计趋势"
            ec_left1.setOption(ec_left1_option)
        },
        error: function (xhr, type, errorThrown) {

        }
    })
}

function get_l2_data() {
    $.ajax({
        url: "/l2?region=" + sessionStorage.getItem("region"),
        timeout: 10000,
        success: function (data) {
            ec_left2_option.xAxis.data = data.days
            ec_left2_option.series[0].data = data.dignose
            ec_left2_option.series[1].data = data.heal
            ec_left2_option.series[2].data = data.dead
            ec_left2_option.title.text = sessionStorage.getItem("region")==="china"?"全国新增趋势":"全球新增趋势"
            ec_left2.setOption(ec_left2_option)
        },
        error: function (xhr, type, errorThrown) {

        }
    })
}

function get_r1_data() {
    $.ajax({
        url: "/r1?region=" + sessionStorage.getItem("region"),
        timeout: 10000,
        success: function (data) {
            ec_right1_option.xAxis[0].data = data.keys
            ec_right1_option.series[0].data = data.values
            ec_right1_option.title.text = sessionStorage.getItem("region")==="china"?"全国地区现存确诊人数top10":"全球地区累计确诊人数top10"
            ec_right1.setOption(ec_right1_option)
        },
        error: function (xhr, type, errorThrown) {

        }
    })
}

function get_r2_data() {
    $.ajax({
        url: "/r2?region=" + sessionStorage.getItem("region"),
        timeout: 10000,
        success: function (data) {
            var template = "<h2 style='color: white'>最新新闻</h2>"
            var data = data.data
            for (index in data) {
                var url_info = data[index]
                var a_label = `<li><a href='${url_info.value}'style="text-decoration:underline;color: white;margin-top: 1px">${url_info.name}</a></li>`
                template += a_label
            }
            document.getElementById("r2").innerHTML = template

        },
        error: function (xhr, type, errorThrown) {

        }
    })
}

function change_region() {
    if (sessionStorage.getItem("region") === "china") {
        sessionStorage.setItem("region", "world")
        document.getElementById("title").innerText = "全球疫情大数据可视化"
    } else {
        sessionStorage.setItem("region", "china")
        document.getElementById("title").innerText = "全国疫情大数据可视化"
    }
    get_c1_data()
    get_c2_data()
    get_l1_data()
    get_l2_data()
    get_r1_data()
    get_r2_data()
}

function showTime() {
    let nowtime = new Date();
    let year = nowtime.getFullYear();
    let month = nowtime.getMonth() + 1;
    let date = nowtime.getDate();
    document.getElementById("time").innerText = year + "-" + month + "-" + date + " " + nowtime.toLocaleTimeString();
}

if (!sessionStorage.getItem("region")) {
    sessionStorage.setItem("region", "china")
}
get_c1_data()
get_c2_data()
get_l1_data()
get_l2_data()
get_r1_data()
get_r2_data()
setInterval(showTime, 1000)
//根据窗口的大小变动图表
window.onresize = function () {
    ec_center.resize();
    ec_left1.resize();
    ec_left2.resize();
    ec_right2.resize();
    ec_right1.resize();
}