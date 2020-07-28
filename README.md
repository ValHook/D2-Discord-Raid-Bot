# D2 Discord Raid Bot

[![Build Status](https://travis-ci.org/ValHook/D2-Discord-Raid-Bot.svg?branch=master)](https://travis-ci.org/ValHook/D2-Discord-Raid-Bot.svg?branch=master)

A useful chat bot to organize Destiny 2 raids in a Discord server.

### Usage
TODO: Write examples

### Build

You must have the following dependencies installed:
1. python3
2. bazel

Set your bungie API key and discord token in an environment variable:
```sh
export BUNGIE_API_KEY=...
export DISCORD_TOKEN=...
```

### Run
```sh
bazel run //bot
```

### Tests
Run all the workspace tests:
```sh
./check_tests.sh
```

Run linter checks (Only bazel and python files, no support for protos yet):
```sh
./check_lint.sh
```

Attempt fixing some of the lint mistakes (Only Bazel files, no support for python or protos yet):
```sh
./perform_lint.sh
```

