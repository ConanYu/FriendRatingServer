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
], 'atcoder', 'cppisgood', 'https://atcoder.jp/users/cppisgood');
*/
function generateGraph(dom, data, oj_name, username, user_info_url) {
    // 基于准备好的dom，初始化echarts实例
    let myChart = echarts.init(dom);

    // function unixstampToDate(time) {
    //     console.log(new Date(time * 1000).toLocaleDateString().replaceAll('/', '-'))
    //     return new Date(time * 1000).toLocaleDateString().replaceAll('/', '-');
    // }

    let ret = [null, null];
    if (oj_name === 'atcoder') {
        ret = get_line_graph_background_data(atcoder_ratings, getAtcoderRatingColor);
    } else if (oj_name === 'codeforces') {
        ret = get_line_graph_background_data(codeforces_ratings, getCodeforcesRatingColor);
    } else if (oj_name === 'nowcoder') {
        ret = get_line_graph_background_data(nowcoder_ratings, getNowcoderRatingColor);
    }

    let background_data = ret[0], markline_data = ret[1];

    // 指定图表的配置项和数据
    let option = {
        title: {
            text: username,
            link: user_info_url,
        },
        legend: {},
        toolbox: {
            feature: {
                saveAsImage: {
                    name: oj_name + ' ' + username,
                    pixelRatio: 2
                }
            }
        },
        grid: [
            {
                show: true,
                // left: '20%',
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
        series: [
            {
                lineStyle: {
                    color: 'gold',
                    shadowColor: 'white',
                    shadowBlur: 1
                },
                itemStyle: {
                    color: 'gold',
                    shadowColor: 'white',
                    shadowBlur: 1
                },
                name: oj_name,
                type: 'line',
                data: data,
                encode: {
                    x: 0,
                    y: 1,
                },
                markPoint: {
                    symbol: 'circle',
                    symbolSize: 10,
                    silent: true,
                    data: [
                        {
                            type: 'max',
                            label: {
                                position: 'top',
                                textBorderWidth: 5,
                            }
                        },
                    ]
                },
                markArea: {
                    silent: true,
                    data: background_data
                },

                markLine: {
                    silent: true,
                    symbol: 'none',
                    label: {
                        position: 'start',
                    },
                    lineStyle: {
                        type: 'solid',
                        width: 0,
                    },
                    data: markline_data,
                },
            },
        ],
        tooltip: {
            backgroundColor: '#222',
            borderColor: '#777',
            formatter: function (obj) {
                var value = obj.value;
                return '<div style="border-bottom: 1px solid rgba(255,255,255,.3); font-size: 18px;padding-bottom: 7px;margin-bottom: 7px">'
                    + value[3] + '<br>'
                    + 'rating: ' + value[1]
            },
            position: 'right',
        },
        dataZoom: {
            type: 'slider'
        }
    };

    myChart.on('click', function (params) {
        window.open(params.value[4]);
    });

    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}

function generateLineGraph(dom, data, oj_name, username, user_info_url) {
    let myChart = echarts.init(dom);
    let min_val = null;
    let max_val = null;
    if (data.length !== 0) {
        min_val = data[0][0];
        max_val = data[data.length - 1][0];
    }
    let sum = 0;
    for (let item of data) {
        sum += item[1];
    }
    let option = {
        title: {
            text: username,
            link: user_info_url,
            subtext: '总题数: ' + sum,
        },
        toolbox: {
            feature: {
                saveAsImage: {
                    pixelRatio: 2
                }
            }
        },
        tooltip: {
            trigger: 'item',
            axisPointer: {
                type: 'shadow'
            },
            position: 'right',
            formatter: function (obj) {
                var value = obj.value;
                return '<div style="border-bottom: 1px solid rgba(255,255,255,.3); font-size: 18px;padding-bottom: 0px;margin-bottom: 0px">'
                    + '分数: ' + value[0] + '<br>'
                    + '过题数: ' + value[1]
                    + '</div>'
            },
        },
        grid: {
            top: '20%',
        },
        dataZoom: [{
            type: 'inside'
        }, {
            type: 'slider'
        }],
        xAxis: {
            name: '分数',
            type: 'value',
            silent: false,
            splitLine: {
                show: false
            },
            splitArea: {
                show: false
            },
            minInterval: 100,
            min: min_val - 100,
            max: max_val + 100,
        },
        yAxis: {
            name: '过题数',
            splitArea: {
                show: false
            }
        },
        legend: {},
        series: [{
            type: 'bar',
            data: data,
            name: oj_name,
            large: true,
            itemStyle: {
                normal: {
                    label: {
                        show: true, //开启显示
                        position: 'top', //在上方显示
                        textStyle: { //数值样式
                            color: 'black',
                        }
                    }
                }
            }
        }],
        min: min_val,
        max: max_val,
        visualMap: {
            show: false,
            orient: 'horizontal',
            left: 'center',
            min: min_val,
            max: max_val,
            text: ['High Score', 'Low Score'],
            // Map the score column to color
            dimension: 0,
            inRange: {
                color: ['green', 'red']
            }
            
        },
    };
    myChart.setOption(option);
}