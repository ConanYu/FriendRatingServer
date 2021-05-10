/*
data: [[date, high_rating, point_rating, contest_name, contest_url],...]

generateGraph(document.getElementById('main'), [
            ["2019-9-1", 173, 173, "AtCoder Beginner Contest 139", "https://atcoder.jp/contests/abc139/standings?watching=cppisgood"],
            ["2019-9-7", 252, 252, "AtCoder Beginner Contest 140", "https://atcoder.jp/contests/abc140/standings?watching=cppisgood"],
            ["2019-9-28", 507, 507, "AtCoder Beginner Contest 142", "https://atcoder.jp/contests/abc142/standings?watching=cppisgood"],
            ["2019-10-19", 1560, 1560, "AtCoder Beginner Contest 143", "https://atcoder.jp/contests/abc143/standings?watching=cppisgood"],
            ["2019-10-27", 721, 721, "AtCoder Beginner Contest 144", "https://atcoder.jp/contests/abc144/standings?watching=cppisgood"],
            ["2020-1-26", 2842, 2842, "AtCoder Beginner Contest 153", "https://atcoder.jp/contests/abc153/standings?watching=cppisgood"],
            ["2020-9-13", 1669, 1669, "AtCoder Beginner Contest 178", "https://atcoder.jp/contests/abc178/standings?watching=cppisgood"]
        ], 'atcoder', 'cppisgood');
*/
function generateGraph(dom, data, oj_name, username) {
    // 基于准备好的dom，初始化echarts实例
    let myChart = echarts.init(document.getElementById(dom.id));

    // function unixstampToDate(time) {
    //     console.log(new Date(time * 1000).toLocaleDateString().replaceAll('/', '-'))
    //     return new Date(time * 1000).toLocaleDateString().replaceAll('/', '-');
    // }

    let ret = null;
    if (oj_name === 'atcoder') {
        ret = get_line_graph_background_data(atcoder_ratings, getAtcoderRatingColor);
    } else if (oj_name === 'codeforces') {
        ret = get_line_graph_background_data(codeforces_ratings, getCodeforcesRatingColor);
    }

    let background_data = ret[0], visual_map_pieces = ret[1];

    // 指定图表的配置项和数据
    let option = {
        title: {
            text: username
        },
        tooltip: {},
        legend: {},
        grid: [
            {
                show: true,
                left: '20%',
            }
        ],
        xAxis: [
            {
                type: 'time',
                splitNumber: 13,
                gridIndex: 0
            }
        ],
        yAxis: [
            {
                show: false,
                scale: true,
                gridIndex: 0
            },
        ],
        lineStyle: {
            color: 'purple'
        },
        series: [
            {
                name: oj_name,
                type: 'line',
                data: data,
                encode: {
                    x: 0,
                    y: 1,
                },
                markArea: {
                    silent: true,
                    data: background_data
                }
            },
        ],
        visualMap: [
            {
                pieces: visual_map_pieces,
                left: '0%',
                top: '25%'
            }
        ],
        tooltip: {
            padding: 10,
            backgroundColor: '#222',
            borderColor: '#777',
            borderWidth: 1,
            formatter: function (obj) {
                var value = obj.value;
                return '<div style="border-bottom: 1px solid rgba(255,255,255,.3); font-size: 18px;padding-bottom: 7px;margin-bottom: 7px">'
                    + value[3] + '<br>'
                    + 'rating: ' + value[1]
            }
        },
    };

    myChart.on('click', function (params) {
        window.open(params.value[4]);
    });

    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}