#!/bin/sh

# Delete the avids from file on STDIN.
#
# As yet this is very simple and not hugely
# robust. It is waiting for test data.

DATABASE=avox

while read AVID; do \
    echo $AVID
    echo "DELETE FROM $DATABASE WHERE avid=$AVID;" | mysql avox
done
