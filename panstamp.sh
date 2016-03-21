#! /bin/sh
### BEGIN INIT INFO
# Provides:          panstamp
# Required-Start:
# Required-Stop:
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Run lagarto and node-red
# Description:
### END INIT INFO

LAGARTO_SWAP=/home/debian/python_tools/lagarto/lagarto-swap/lagarto-swap.py
#LAGARTO_SWAP=/home/pi/python/lagarto/lagarto-swap/lagarto-swap.py

case "$1" in
  start)
  echo "Starting lagarto-swap"
  python $LAGARTO_SWAP &
  ;;
  stop)
  echo "Killing all python processes"
  killall python
  ;;
esac

exit 0

