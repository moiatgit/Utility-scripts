#! /usr/bin/env python
# encoding: utf-8

# This script takes a .rst file as first argument and converts it to a
# markdown with the same name and extension .md prepared for being
# used at ruhoh blogs

# required: docutils

# TODO: when referencing local documents from other documents there's
# a mismatch between urls: rst files should reference to other rst
# files but ruhoh requires {{url}}/category/title as href. To solve
# it, it is necessary a not-so-hard change: 
#  check whether the link hrefs to a local .rst file
#  then extract from the referenced file the title and the category
#  then replace the link to {{url}}/categories/title.

# In the meantime, a simple workaround is hardcoding ruhoh's expected
# href in the rst file.

# You might want to allow completion for this script. Put the
# following code somewhere accessible by your .bashrc or source it

#   _rst2ruhoh()
#   {
#       local cur
#       COMPREPLY=()
#       _get_comp_words_by_ref cur
#
#       _filedir rst
#   }
#   complete -o default -o nospace -F _rst2ruhoh  rst2ruhoh.py

#
import os, shutil, sys, re, datetime
from BeautifulSoup import BeautifulSoup, Comment
from docutils.core import publish_cmdline, default_description
from ConfigParser import ConfigParser
import argparse
import tempfile
#
CONF_FILENAME = os.path.expanduser("~/.rst2ruhoh")  # configuration filename
#
def getMetaInfo(soup):
    """ get all meta information included in soup and returns it in a list """
    meta = []
    for comment in soup.findAll(text=lambda text:isinstance(text, Comment)):
        c = str(comment).lstrip("<!--").rstrip("-->").strip()
        if re.match("\w+: .+", c):  # is a setting
            meta.append(c)
            comment.extract()
    return meta
#
def extractTitle(soup):
    """ removes title from soup and returns it.
        It returns empty string when no title is found. """
    title = soup.find("h1")
    if title.has_key("class"):
        result = title.text.encode('utf-8')
        title.extract()
    else:
        result = ''
    return result
#
def addMetaIfMissing(meta, tag, val):
    """ adds new tag to meta list with val if it is not already there """
    for m in meta:
        if m.startswith(tag):
            break
    else:
        meta.insert(0, "%s: %s"%(tag, val))
#
def create_md(html_filename, ruhoh_path, rst_filename, draft):
    """ creates the md file from html.
        If draft, it creates the document with draft option """
    html = open(html_filename).read()
    soup = BeautifulSoup(html)
    soup = soup.body.contents[1]    # cleaned up to body
    meta = getMetaInfo(soup)

    title = extractTitle(soup) # remove title
    if title:
        addMetaIfMissing(meta, 'title', title)

    # set date if not present in meta
    for m in meta:
        if m.startswith("date"):
            m.replace('"', "'")
            break;
    else:
        meta.insert(1, "date: '%s'"%datetime.date.today().strftime("%Y-%m-%d"))
    #
    # get post category
    for m in meta:
        if m.startswith("categories"):
            category = m.lstrip("categories:").strip()
            dest_path = os.path.join(ruhoh_path, "posts", category)
            path_media = os.path.join(ruhoh_path, "media", category)
            break
    else:
        category = ""
        dest_path = os.path.join(ruhoh_path, "posts")
        path_media = os.path.join(ruhoh_path, "media")
    # set draft option
    if draft:
        for m in meta:
            if m.startswith("type:"):
                break
        else:
            meta.insert(1, "type: draft")
    # source path
    src_path = os.path.dirname(rst_filename)
    # image path correction
    for img in soup.findAll("img"):
        img_path = os.path.join(src_path, img["src"])
        if os.path.exists(img_path):
            if not os.path.exists(path_media):
                os.mkdir(path_media)
            shutil.copy(img_path, path_media)
            if category == "":
                img["src"]="{{urls.media}}/%s"%img["src"]
            else:
                img["src"]="{{urls.media}}/%s/%s"%(category, img["src"])
        else:
            print >> sys.stderr, "WARNING: file %s not found but linked"%img["src"]
        #
    # other resources correction
    for a in soup.findAll("a"):
        if a.has_key("href"):
            resource_path = os.path.join(src_path, a["href"])
            if os.path.exists(resource_path):
                if not os.path.exists(path_media):
                    os.mkdir(path_media)
                shutil.copy(resource_path, path_media)
                if category == "":
                    a["href"]="{{urls.media}}/%s"%a["href"]
                else:
                    a["href"]="{{urls.media}}/%s/%s"%(category, a["href"])
    # create category folder if doesn't exists
    if not os.path.exists(dest_path):
        os.mkdir(dest_path)
    # compose md name
    name, _ = os.path.splitext(os.path.basename(rst_filename))
    md_filename = os.path.join(dest_path, "%s.md"%name)
    # write results on md_file
    md = open(md_filename, "w")
    md.write("---\n")
    for m in meta:
        md.write("%s\n"%m)
    md.write("---\n\n")
    md.write(str(soup))
    md.close()
#
def setLocale():
    """ tries to set locale """
    try:
        import locale
        locale.setlocale(locale.LC_ALL, '')
    except:
        pass
#
def checkParams():
    """ checks that the arguments of the program call, and the
    configuration file are as expected. 
    In case something's wrong, an error missage is issued and 
    finishes execution with an error code.
    When everything is ok, it returns the configuration information
    in a tuple: rst_filename, ruhoh_path """
    p = argparse.ArgumentParser(description="Converts from rst to ruhoh format", version="1.0")
    p.add_argument('paths', metavar='path', nargs='+', help="Source file path with .rst extension")
    p.add_argument("-d", "--draft", action="store_true", help="Mark converted file as draft", dest="draft")
    p.add_argument("-r", "--ruhoh_path", action="store", help="Path to ruhoh local copy. Overrides config file specs.", dest="ruhoh_path")
    options = p.parse_args()
    #
    sourcelist = options.paths
    #
    for source in sourcelist:
        path, ext = os.path.splitext(source)
        if ext != ".rst":
            print >> sys.stderr, "Error: .rst extension expected in %s"%source
            sys.exit(2)
        #
        if not os.path.exists(source):
            print >> sys.stderr, "Error: file not found: %s"%source
            sys.exit(4)
    #
    if options.ruhoh_path:
        ruhoh_path = options.ruhoh_path
    else:
        # check configuration file
        c = ConfigParser()
        try:
            c.read(CONF_FILENAME)
            ruhoh_path = os.path.expanduser(c.get('RUHOH', 'local_path'))
        except:
            print >> sys.stderr, "Error: %s expected with contents\n"%CONF_FILENAME +\
                    "[RUHOH]\n" +\
                    "local_path = path/to/ruhoh/local/site"
            sys.exit(3)
    #
    if not os.path.exists(ruhoh_path):
        print >> sys.stderr, "Error: file not found: %s"%ruhoh_path
        sys.exit(5)
    #
    draft = options.draft
    #
    return sourcelist, ruhoh_path, draft
#
def main():

    # try to set locale
    setLocale()

    # get configuration information
    sourcelist, ruhoh_path, draft = checkParams()

    for rst_filename in sourcelist:
        # prepare params for docutils
        sys.argv = [sys.argv[0], rst_filename]

        # define html output filename for docutils
        html_file = tempfile.NamedTemporaryFile()
        html_filename = html_file.name
        sys.argv.append(html_filename)

        # generate html conversion
        description = ('Generates ruhoh\'s md documents from standalone '
                       'reStructuredText sources.  ' + default_description)
        publish_cmdline(writer_name='html', description=description)

        # create md for ruhoh
        create_md(html_filename, ruhoh_path, rst_filename, draft)
        #
    return 0
#
if __name__=="__main__":
    sys.exit(main())

