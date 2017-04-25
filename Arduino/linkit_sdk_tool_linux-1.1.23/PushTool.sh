#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
"$DIR/uploader.py" -v -v -v -v -clear -port $1 -app $2
