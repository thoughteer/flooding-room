#!/bin/bash

python -m floodingroom.api &
python -m floodingroom.server &

. maintenance/common/hold.sh
exit 0
