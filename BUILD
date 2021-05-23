load("@rules_python//python:defs.bzl", "py_binary")
load("@rules_python//python:pip.bzl", "pip_install")

pip_install(
   name = "friend_rating_server_deps",
   requirements = "//:requirements.txt",
)

py_binary(
    name = "friend_rating_server_bin",
    srcs = ["friend_rating_server/**/*.py"],
    deps = ["//:friend_rating_server_deps"],
    imports = ["."],
)
