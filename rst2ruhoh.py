#! /usr/bin/env python
# encoding: utf-8
#
# This script takes a .rst file as first argument and converts it to 
# a markdown with the same name and extension .md prepared for being
# used at ruhoh blogs
#
# required: docutils

# TODO: when referencing local documents from other documents there's a mismatch
# between urls: rst files should reference to other rst files but ruhoh requires
# {{url}}/category/title as href. To solve it, it is necessary 
# a not-so-hard change: check whether the link hrefs to a local .rst file. Then
# try to extract from the referenced file the title and the category. Then replace
# the link to {{url}}/categories/title.
# In the meantime, a simple workaround is hardcoding ruhoh's expected href
# in the rst file.
# 
# TODO: this is a rather Q&D version. You might want to clean it up 
# before someone's comments turn your face red :s

#
import os, shutil, sys, re, datetime
from BeautifulSoup import BeautifulSoup, Comment
from docutils.core import publish_cmdline, default_description
from ConfigParser import ConfigParser
#
CONF_FILENAME = os.path.expanduser("~/.rst2ruhoh")  # configuration filename
#
def compose_tmp_name(rst_filename):
    """ from rst filename composes a html temporal file name
        hopefuly difficult to collide with an existing one """
    name, _ = os.path.splitext(os.path.basename(rst_filename))
    d = datetime.datetime.isoformat(datetime.datetime.now())
    return "/tmp/%s_%s.html"%(d, name)
#
def create_md(html_filename, ruhoh_path, rst_filename):
    """ creates the md file from html """
    html = open(html_filename).read()
    soup = BeautifulSoup(html)
    soup = soup.body.contents[1]    # cleaned up to body
    # get meta information
    meta = []
    for comment in soup.findAll(text=lambda text:isinstance(text, Comment)):
        c = str(comment).lstrip("<!--").rstrip("-->").strip()
        meta.append(c)
        comment.extract()
    # remove title
    title = soup.find("h1")
    if title.has_key("class"):
        # in case meta has no title, this title will be set.
        for m in meta:
            if m.startswith("title"):
                break
        else:
            meta.insert(0, "title: %s"%title.text.encode('utf-8'))
        title.extract()
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
    # check arguments and config file
    if len(sys.argv) != 2:
        print >> sys.stderr, "Usage: %s rst_filepath"%sys.argv[0]
        sys.exit(1)
    #
    path, ext = os.path.splitext(sys.argv[1])
    if ext != ".rst":
        print >> sys.stderr, "Error: rst extension expected"
        sys.exit(2)
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
    if not os.path.exists(sys.argv[1]):
        print >> sys.stderr, "Error: file not found: %s"%sys.argv[1]
        sys.exit(4)
    if not os.path.exists(ruhoh_path):
        print >> sys.stderr, "Error: file not found: %s"%ruhoh_path
        sys.exit(5)
    #
    return sys.argv[1], ruhoh_path
#
def main():

    # try to set locale
    setLocale()

    # get configuration information
    rst_filename, ruhoh_path = checkParams()

    # define html output filename for docutils
    html_filename = compose_tmp_name(rst_filename)
    sys.argv.append(html_filename)

    # generate html conversion
    description = ('Generates ruhoh\'s md documents from standalone '
                   'reStructuredText sources.  ' + default_description)
    publish_cmdline(writer_name='html', description=description)

    # create md for ruhoh
    create_md(html_filename, ruhoh_path, rst_filename)
    return 0
#
if __name__=="__main__":
    sys.exit(main())

