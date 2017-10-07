#!/bin/bash

# (cd floodingroom/client && npm install)

if [ -z "$1" ]
then
    python -m floodingroom.server &
else
    python -m floodingroom.$1 &
fi

. maintenance/common/hold.sh
exit 0
