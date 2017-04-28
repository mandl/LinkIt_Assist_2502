#!/bin/sh

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
"$DIR/uploader.py" $1 $2 $3 $4 $5 $6 -v -v -v -v
