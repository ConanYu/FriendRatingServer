let app_data = {
    show: {},
    cls: {},
    dict: {},
    table: {},
    members: members,
    sortStatus: '',
};

let platforms = [
    "codeforces",
    "atcoder",
    "nowcoder",
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
            showRow: function (index) {
                let is_show_before = app_data.show["graph_" + index + "_show"];
                showInit();
                app_data.show["graph_" + index + "_show"] = !is_show_before;
            },
            sortCol: function (platform) {
                app_data.members.sort(function (a, b) {
                    return app_data.table[a.index][platform + "_contest"].rating - app_data.table[b.index][platform + "_contest"].rating;
                });
                if (app_data.sortStatus !== platform + "_desc") {
                    app_data.members.reverse();
                    app_data.sortStatus = platform + "_desc";
                } else {
                    app_data.sortStatus = platform + "_inc";
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
