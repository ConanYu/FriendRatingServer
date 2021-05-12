let app_data = {
    show: {},
    cls: {},
};

let platforms = [
    "codeforces",
    "atcoder",
];

for (let member of members) {
    app_data["show"]["graph_" + member["index"] + "_show"] = false;
    for (let platform of platforms) {
        app_data["show"]["graph_" + member["index"] + "_" + platform + "_show"] = false;
        app_data["cls"]["btn_" + member["index"] + "_" + platform] = "btn btn-sm border";
    }
}

function loadGraph() {
    for (let member of members) {
        for (let platform of platforms) {
            let graph_id = "graph-" + member["index"] + "-" + platform;
            if (member[platform + "_data"]) {
                let data = [];
                for (let contest of member[platform + "_data"]["data"]) {
                    let date = new Date(contest["timestamp"] * 1000);
                    let rating = contest["rating"];
                    let name = contest["name"];
                    let url = contest["url"];
                    data.push([
                        "" + date.getFullYear() + "-" + date.getMonth() + "-" + date.getDay(),
                        rating,
                        rating,
                        name,
                        url,
                    ]);
                }
                data.sort(function (a, b) {
                    return a[0] - b[0];
                });
                generateGraph(
                    document.getElementById(graph_id),
                    data,
                    platform,
                    member[platform + "_name"],
                    member[platform + "_profile_url"]);
            }
        }
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
   var url = location.search; //获取url中"?"符后的字串
   var theRequest = {};
   if (url.indexOf("?") !== -1) {
      var str = url.substr(1);
      strs = str.split("&");
      for(var i = 0; i < strs.length; i ++) {
         theRequest[strs[i].split("=")[0]]=(strs[i].split("=")[1]);
      }
   }
   return theRequest;
}

let app = new Vue({
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
            }
        },
        showRow: function (index) {
            let is_show_before = app_data.show["graph_" + index + "_show"];
            showInit();
            app_data.show["graph_" + index + "_show"] = !is_show_before;
        },
        sortCol: function (col) {
            let requestData = getRequestData();
            let desc = 0;
            if (requestData.sortBy === col && requestData.desc) {
                desc = requestData.desc;
            }
            desc = 1 - desc;
            window.location.replace("/?sortBy=" + col + "&desc=" + desc.toString());
        },
    },
    mounted: function () {
        this.$nextTick(loadGraph);
    },
});

