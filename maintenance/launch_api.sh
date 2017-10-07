#!/bin/bash

python -m floodingroom.api &

. maintenance/common/hold.sh
exit 0
