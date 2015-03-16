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
#    GITHUBDIR          path to GitHub repository
#    PELICANOPTS        additional pelican options (could be blank)
#    PELICANCONF        file name of the pelican standard
#                       configuration file
#    PUBLISHCONF        file name of the pelican configuration file
#                       for publishing
#

# TODO: Current implementation does not have into account whether the
# files in GITHUBDIR have been actually pushed onto GitHub For that
# reason it is possible to cancel pushing while having commited last
# changes. Further calls to this script (without changes on contents)
# will not be pushed since there will not be any change on git rep.
# You might want to include a certain file flag (git unmanaged) that
# is created after actual commit and removed just when actual push
#


P2HCONFIG=~/.pelican2github
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

echo "Removing broken links on $INPUTDIR"
find -L $INPUTDIR -type l -exec rm -v {} +
#
if [[ "$*" == *$PUBLISHOPT* ]]
then
    PUBLISH=yes
    CONFFILE=$PELICANDIR/$PUBLISHCONF
else
    PUBLISH=no
    CONFFILE=$PELICANDIR/$PELICANCONF
    echo "Remember: include $PUBLISHOPT option to send it to GitHub"
fi
#
# elements to preserve on GITHUBDIR in "find" notation
CLEANEXCEPTIONS="( -not -name index.php -and -not -name .htaccess -and -not -wholename */.git* )"
#

# remove static contents from output
find $OUTPUTDIR -mindepth 1 -delete
echo "$OUTPUTDIR is now clean"
#

# convert contents
cd $PELICANDIR
pelican -o $OUTPUTDIR -s $CONFFILE $PELICANOPTS $INPUTDIR 

# cleaning up previous contents on GitHub's dir
find $GITHUBDIR -mindepth 1 $CLEANEXCEPTIONS -delete
echo "$GITHUBDIR is now clean"

# copying contents into GitHub's dir
echo "copying contents into GitHub's dir"
cd $GITHUBDIR
git checkout gh-pages &> /dev/null
cp -r $OUTPUTDIR/* $GITHUBDIR
echo "$GITHUBDIR now contains an updated copy of the site"

# end execution when it is not to be published
[[ $PUBLISH == "no" ]] && exit 0

# commiting any change to git
find . -type d | grep -v "\.\w" | sed "s/\(.*\)/\"\1\"/g" | xargs git add -A
TMPFILE="/tmp/pelican2github_`date`.$RANDOM"
git commit -am "automated commit for GitHub on `date`" &> "$TMPFILE"

if [[ -n $(grep "nothing to commit (working directory clean)" "$TMPFILE") ]];
then
    echo "No changes to be send to GitHub"
else
    # send it to GitHub
    git push origin gh-pages
fi
rm "$TMPFILE"

