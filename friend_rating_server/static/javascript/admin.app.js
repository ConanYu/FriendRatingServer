let app_data = {
    members: [],
    add_member: {
        name: "",
        grade: "",
        codeforces: "",
        atcoder: "",
        nowcoder: "",
    },
};

new Vue({
    delimiters: ["${", "}$"],
    el: "#app",
    data: app_data,
    methods: {
        deleteMember: function (index, name) {
            let qs = Qs;
            axios.post('/api/delete_member', qs.stringify({
                "index": index,
                "name": name,
            })).then(res => {
                location.reload();
            });
        },
        addMember: function () {
            let qs = Qs;
            axios.post('/api/add_member', qs.stringify({
                "name": app_data.add_member.name,
                "grade": app_data.add_member.grade,
                "codeforces": app_data.add_member.codeforces,
                "atcoder": app_data.add_member.atcoder,
                "nowcoder": app_data.add_member.nowcoder,
                "luogu": app_data.add_member.luogu,
                "vjudge": app_data.add_member.vjudge,
            })).then(res => {
                location.reload();
            }).catch(err => {
                alert(err);
            });
        },
    },
});

axios.get('/api/get_members').then(res => {
    app_data.members = res.data;
});
