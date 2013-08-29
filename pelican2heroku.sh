#! /bin/bash
#
# This script converts pelican contents at INPUTDIR and leaves
# converted static html contents on OUTPUTDIR.
# 
# Everytime it is call, it removes all the contents on OUTPUTDIR
# except for CLEANEXCEPTIONS and runs pelican script on INPUTDIR
#

# the following vars should appear in the file ~/.pelican2heroku
#    PELICANDIR         path to pelican base dir
#    INPUTDIR           path to pelican contents dir
#    OUTPUTDIR          path to pelican output dir
#    HEROKUDIR          path to heroku repository
#    PELICANOPTS        additional pelican options (could be blank)
#    PELICANCONF        file name of the pelican standard
#                       configuration file
#    PUBLISHCONF        file name of the pelican configuration file
#                       for publishing
#
#

P2HCONFIG=~/.pelican2heroku
PUBLISHOPT="--publish"
#
# exit when no configuration found
if [ ! -f  "$P2HCONFIG" ]
then
    echo "ERROR: configuration file not found: $P2HCONFIG"
    exit 1
fi

# load configuration vars
source $P2HCONFIG

#
if [[ "$*" == *$PUBLISHOPT* ]]
then
    PUBLISH=yes
    CONFFILE=$PELICANDIR/$PUBLISHCONF
else
    PUBLISH=no
    CONFFILE=$PELICANDIR/$PELICANCONF
    echo "Remember: include $PUBLISHOPT option to send it to heroku"
fi
#
CLEANEXCEPTIONS="( -not -name index.php -and -not -name .htaccess -and -not -wholename */.git* )"
#

# remove static contents from output
find $OUTPUTDIR -mindepth 1 -delete
echo "$OUTPUTDIR is now clean"
#

# convert contents
pelican -o $OUTPUTDIR -s $CONFFILE $PELICANOPTS $INPUTDIR 

# cleaning up previous contents on heroku's dir
find $HEROKUDIR -mindepth 1 $CLEANEXCEPTIONS -delete
echo "$HEROKUDIR is now clean"

# copying contents into heroku's dir
cd $HEROKUDIR
cp -ru $OUTPUTDIR/* $HEROKUDIR
echo "$HEROKUDIR now contains an updated copy of the site"

# end execution when it is not to be published
[[ $PUBLISH == "no" ]] && exit 0

# commiting any change to git
find . -type d | grep -v "\.\w" | sed "s/\(.*\)/\"\1\"/g" | xargs git add -A
TMPFILE="/tmp/`date`.$RANDOM"
git commit -am "automated commit for heroku on `date`" | tee "$TMPFILE"
RESULT=`tail -1 "$TMPFILE"`
if [[ "$RESULT" == "nothing to commit"* ]]
then
    echo "No changes to be send to heroku"
    exit 0
fi
rm "$TMPFILE"

# send it to heroku
git push heroku master
