#!/usr/bin/env bash

set -e
set -x

mypy app
ruff check app scripts
ruff format app --check
