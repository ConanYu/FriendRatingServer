load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")

git_repository(
    name = "friend_rating_rpc",
    remote = "https://github.com/cppisgood/FriendRatingRPC.git",
    branch = "master",
)

git_repository(
    name = "rules_python",
    remote = "https://github.com/bazelbuild/rules_python.git",
    tag = "0.2.0",
)

load("@rules_python//python:pip.bzl", "pip_install")

pip_install(
   name = "friend_rating_server_deps",
   requirements = "//:requirements.txt",
)
