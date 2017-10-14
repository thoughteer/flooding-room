#!/bin/bash

#(cd floodingroom/client && npm install)

python -m floodingroom.server &

. maintenance/common/hold.sh
exit 0
