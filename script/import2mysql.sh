#!/bin/sh -e
# as root
# copy in the data file to /var/lib/mysql/avox as avox.txt
# then in /var/lib/mysql/avox run
# mysqlimport -u avox -r --fields-terminated-by='~' avox avox.txt

# to make this work we need a way of calculating the value of the
# extract

FRUITFILE=/home/avox/tiddlywebs/www.wiki-data.com/templates/fruitmachine.html

DATABASE=avox
DATAUSER=avox
DATATABLE=avox
DATAFILE=avox.txt
DATADIR=/var/lib/mysql/avox
EXTRACTDIR=${2:-/home/avox/wikidata/avoxjson-s/dataextracts}

## calculate extract
## XXX not done!!!
EXTRACTFILE=${1:?"filename required"}

# If this is a full file, delete all the existing entries.
echo $EXTRACTFILE | grep 'wiki_full' && echo "delete from $DATATABLE;" \
    | mysql -u $DATAUSER $DATABASE

cd $DATADIR
cp $EXTRACTDIR/$EXTRACTFILE $DATAFILE

mysqlimport -u $DATAUSER -r --fields-terminated-by='~' $DATABASE $DATAFILE

rm $DATAFILE

COUNTER=$(echo "select count(*) from $DATATABLE;" | \
	mysql --skip-column-names -u $DATAUSER $DATABASE)

# update the fruitmachine automagically
perl -pi -e "s/counter = '\d+'/counter = '$COUNTER'/" $FRUITFILE

echo "Total records: $COUNTER"
