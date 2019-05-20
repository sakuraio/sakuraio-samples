#!/usr/bin/env bash

mkdir -p build

gox \
--osarch "linux/amd64 windows/amd64 darwin/amd64" \
-output="build/{{.Dir}}_{{.OS}}_{{.Arch}}" \
./
