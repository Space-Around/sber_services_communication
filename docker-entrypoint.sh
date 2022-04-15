#!/bin/sh
set -e  # Exit immediately if a command exits with a non-zero status
set -x  # all executed commands are printed to the terminal.

export PYTHONUNBUFFERED=0

case "$1" in
    *)
        exec $@
     ;;
esac
