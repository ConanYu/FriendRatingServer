let app = new Vue({
    delimiters: ["${", "}$"],
    el: "#app",
    methods: {
        test: function () {
            console.log(1);
        },
    },
});