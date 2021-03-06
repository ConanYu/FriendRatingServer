let app_data = {
    show: {},
    cls: {},
    dict: {},
    table: {},
    members: members,
    sortStatus: '',
    is_loading: true,
};

let platforms = [
    "codeforces",
    "atcoder",
    "nowcoder",
    "codeforces_submit",
    "luogu_submit",
    "luogu",
    "vjudge",
    "vjudge_submit",
];

let httpGetPromise = [];

function init() {
    let index = 0;
    for (let member of members) {
        app_data["show"]["graph_" + member["index"] + "_show"] = false;
        app_data["dict"][member["index"]] = index;
        index += 1;
        for (let platform of platforms) {
            app_data["show"]["graph_" + member["index"] + "_" + platform + "_show"] = false;
            app_data["cls"]["btn_" + member["index"] + "_" + platform] = "btn btn-sm border";
        }
        let params = {};
        for (let platform of platforms) {
            params[platform] = member[platform];
        }
        httpGetPromise.push(new Promise((resolve, reject) => {
            axios.get('/api/get_all_data_simple', {
                params: params,
            }).then(res => {
                resolve({
                    data: res.data,
                    index: member.index,
                });
            }).catch(err => {
                reject(err.data)
            });
        }));
    }
}

init();

function loadOneGraph(graph, index, platform) {
    let graph_id = "graph-" + index + "-" + platform;
    if (graph.data) {
        let data = [];
        for (let contest of graph["data"]) {
            let date = new Date(contest["timestamp"] * 1000);
            let rating = contest["rating"];
            let name = contest["name"];
            let url = contest["url"];
            data.push([
                "" + date.getFullYear() + "-" + (date.getMonth() + 1) + "-" + date.getDate(),
                rating,
                rating,
                name,
                url,
            ]);
        }
        generateGraph(
            document.getElementById(graph_id),
            data,
            platform,
            graph["handle"],
            graph["profile_url"]);
    }
}

function loadSubmitGraph(data, index, platform) {
    let graph_id = "graph-" + index + "-" + platform + "_submit";
    if (data.status === 'OK') {
        let distribution = data.data.distribution;
        let arr = [];
        for (let point in distribution) {
            arr.push([parseInt(point, 10), distribution[point]]);
        }
        generateLineGraph(document.getElementById(graph_id), arr, platform, data.handle, data.profile_url);
    }
}

function loadSubmitPieGraph(data, index, platform) {
    let graph_id = "graph-" + index + "-" + platform + "_submit";
    if (data.status === 'OK') {
        let distribution = data.data.oj_distribution;
        let arr = [];
        for (let value in distribution) {
            arr.push({
                value: distribution[value.valueOf()],
                name: value.valueOf(),
            });
        }
        console.log(arr);
        generatePieGraph(document.getElementById(graph_id), arr, data.handle, data.profile_url);
    }
}

function showInit(ignore) {
    for (let key in app_data.show) {
        app_data.show[key.valueOf()] = false;
    }
    for (let key in app_data.cls) {
        app_data.cls[key.valueOf()] = app_data.cls[key.valueOf()].replace(" btn-success", "");
    }
}

function getRequestData() {
    let url = location.search;
    let theRequest = {};
    if (url.indexOf("?") !== -1) {
        let str = url.substr(1);
        let strs = str.split("&");
        for (let i = 0; i < strs.length; i++) {
            theRequest[strs[i].split("=")[0]] = (strs[i].split("=")[1]);
        }
    }
    return theRequest;
}

Promise.all(httpGetPromise).then((value => {
    for (let data of value) {
        app_data.table[data.index.valueOf()] = data.data;
    }
    app_data.is_loading = false;
    new Vue({
        delimiters: ["${", "}$"],
        el: "#app",
        data: app_data,
        methods: {
            showGraph: function (index, platform) {
                let is_show_before = app_data.show["graph_" + index + "_" + platform + "_show"];
                showInit();
                app_data.show["graph_" + index + "_show"] = true;
                app_data.show["graph_" + index + "_" + platform + "_show"] = !is_show_before;
                if (!is_show_before) {
                    app_data.cls["btn_" + index + "_" + platform] += " btn-success";
                    this.$nextTick(function () {
                        axios.get('/api/get_' + platform + "_data", {
                            params: {
                                handle: app_data.members[app_data.dict[index]][platform],
                            },
                        }).then((res) => {
                            loadOneGraph(res.data, index, platform);
                        });
                    });
                }
            },
            showSubmitGraph: function (index, platform) {
                let is_show_before = app_data.show["graph_" + index + "_" + platform + "_submit_show"];
                showInit();
                app_data.show["graph_" + index + "_show"] = true;
                app_data.show["graph_" + index + "_" + platform + "_submit_show"] = !is_show_before;
                if (!is_show_before) {
                    app_data.cls["btn_" + index + "_" + platform + "_submit"] += " btn-success";
                    this.$nextTick(function () {
                        axios.get('/api/get_' + platform + "_submit_data", {
                            params: {
                                handle: app_data.members[app_data.dict[index]][platform],
                            },
                        }).then((res) => {
                            loadSubmitGraph(res.data, index, platform);
                        });
                    });
                }
            },
            showSubmitPieGraph: function (index, platform) {
                let is_show_before = app_data.show["graph_" + index + "_" + platform + "_submit_show"];
                showInit();
                app_data.show["graph_" + index + "_show"] = true;
                app_data.show["graph_" + index + "_" + platform + "_submit_show"] = !is_show_before;
                if (!is_show_before) {
                    app_data.cls["btn_" + index + "_" + platform + "_submit"] += " btn-success";
                    this.$nextTick(function () {
                        axios.get('/api/get_' + platform + "_submit_data", {
                            params: {
                                handle: app_data.members[app_data.dict[index]][platform],
                            },
                        }).then((res) => {
                            loadSubmitPieGraph(res.data, index, platform);
                        });
                    });
                }
            },
            showRow: function (index) {
                let is_show_before = app_data.show["graph_" + index + "_show"];
                showInit();
                app_data.show["graph_" + index + "_show"] = !is_show_before;
            },
            sortRatingCol: function (platform) {
                app_data.members = mergeSort(app_data.members, function (a, b) {
                    let c = app_data.table[a.index][platform + "_contest"].rating;
                    let d = app_data.table[b.index][platform + "_contest"].rating;
                    if (c === undefined) {
                        c = 0;
                    }
                    if (d === undefined) {
                        d = 0;
                    }
                    return c - d;
                }, app_data.sortStatus !== platform + "_contest_desc");
                if (app_data.sortStatus !== platform + "_contest_desc") {
                    app_data.sortStatus = platform + "_contest_desc";
                } else {
                    app_data.sortStatus = platform + "_contest_inc";
                }
                let index = 0;
                for (let member of app_data.members) {
                    app_data["dict"][member["index"]] = index;
                    index += 1;
                }
            },
            sortSubmitCol: function (platform) {
                app_data.members = mergeSort(app_data.members, function (a, b) {
                    let c = app_data.table[a.index][platform + "_submit"].accept_count;
                    let d = app_data.table[b.index][platform + "_submit"].accept_count;
                    if (c === undefined) {
                        c = 0;
                    }
                    if (d === undefined) {
                        d = 0;
                    }
                    return c - d;
                }, app_data.sortStatus !== platform + "_submit_desc");
                if (app_data.sortStatus !== platform + "_submit_desc") {
                    app_data.sortStatus = platform + "_submit_desc";
                } else {
                    app_data.sortStatus = platform + "_submit_inc";
                }
                let index = 0;
                for (let member of app_data.members) {
                    app_data["dict"][member["index"]] = index;
                    index += 1;
                }
            },
            getCodeforcesRatingColor: getCodeforcesRatingColor,
            getAtcoderRatingColor: getAtcoderRatingColor,
        },
    });
}));
