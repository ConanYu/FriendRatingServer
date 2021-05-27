load("@rules_python//python:defs.bzl", "py_binary")

py_binary(
    name = "friend_rating_server_bin",
    srcs = ["friend_rating_server/**/*.py"],
    deps = ["//:friend_rating_server_deps"],
    imports = ["."],
)
