#!/bin/bash

PROJECT_ROOT_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# fuck gitpod
unset PIPENV_VENV_IN_PROJECT
unset PIP_USER
unset PYTHONUSERBASE

kill_pid() {
  if [ -f "$1" ];then
    kill `cat $1` || true
    rm $1
  fi
}
