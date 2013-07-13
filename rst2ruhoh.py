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
class RST2RuhohTranslator:
    def __init__(self, htmlPath, ruhohPath, rstPath, isDraft):
        self.htmlPath  = htmlPath
        self.ruhohPath = ruhohPath
        self.rstPath   = rstPath
        self.isDraft   = isDraft
        self.meta      = {} # includes the meta information of the file

    def translate(self):
        """ performs the translation from rst to ruhoh format. """
        self.setSoupFromHtml()
        self.setMetaInfo()
        self.setTitle()
        self.setCategory()
        self.setPostDate()
        self.setDraftOption()
        self.setDestinationPaths()
        self.fixResourcePaths()

    def saveTranslation(self):
        """ saves the translation in the corresponding destination """
        self.createDestinationPathIfMissing()
        md_filename = self.composeMDFilename()
        self.writeResultsOnFile(md_filename)

    def setDestinationPaths(self):
        """ keeps paths for the destination of the post and media. """
        self.dest_path  = self.composeDestPathFromCategory('posts')
        self.path_media = self.composeDestPathFromCategory('media')

    def setTitle(self):
        """ sets the title of the post """
        title = self.extractTitle()
        if title:
            self.addMetaIfMissing('title', title)

    def addMetaIfMissing(self, tag, val):
        """ adds new tag to meta with val if tag was not already there """
        self.meta[tag] = self.meta.get(tag, val)

    def setPostDate(self):
        """ sets current date as post date if no date is expecified """
        currentDate = "'%s'"%datetime.date.today().strftime("%Y-%m-%d")
        self.addMetaIfMissing('date',currentDate)

    def setDraftOption(self):
        """ sets the draft option if isDraft and draft option is not
            already present """
        if self.isDraft:
            self.addMetaIfMissing('type', 'draft')

    def fixResourcePaths(self):
        """ fixes paths of different resources """
        src_path = os.path.dirname(self.rstPath)
        self.fixImagePaths(src_path)
        self.fixRefPaths(src_path)

    def fixImagePaths(self, path):
        """ fixes paths of images in the post from given path"""
        for img in self.soup.findAll("img"):
            img_path = os.path.join(path, img["src"])
            if os.path.exists(img_path):
                if not os.path.exists(self.path_media):
                    os.mkdir(self.path_media)
                shutil.copy(img_path, self.path_media)
                if self.category == "":
                    img["src"]="{{urls.media}}/%s"%img["src"]
                else:
                    img["src"]="{{urls.media}}/%s/%s"%(self.category, img["src"])
            else:
                print >> sys.stderr, "WARNING: file %s not found but linked"%img["src"]

    def fixRefPaths(self, path):
        """ fixes paths of references to other potts from given path """
        for a in self.soup.findAll("a"):
            if a.has_key("href"):
                resource_path = os.path.join(path, a["href"])
                if os.path.exists(resource_path):
                    if not os.path.exists(self.path_media):
                        os.mkdir(self.path_media)
                    shutil.copy(resource_path, self.path_media)
                    if self.category == "":
                        a["href"]="{{urls.media}}/%s"%a["href"]
                    else:
                        a["href"]="{{urls.media}}/%s/%s"%(self.category, a["href"])

    def setSoupFromHtml(self):
        """ sets soup from the html file """
        html = open(self.htmlPath).read()
        soup = BeautifulSoup(html)
        self.soup = soup.body.contents[1]    # cleaned up to body

    def setMetaInfo(self):
        """ processes all meta information included in soup and 
        includes it in the meta property """
        getComments = lambda text:isinstance(text, Comment)
        for comment in self.soup.findAll(text=getComments):
            c = str(comment).lstrip("<!--").rstrip("-->").strip()
            m = re.match("(\w+): (.+)", c)
            if m:  # is a setting
                metaItem  = m.group(1)
                metaValue = m.group(2)
                self.meta[metaItem]=metaValue
                comment.extract()

    def createDestinationPathIfMissing(self):
        """ create category folder if doesn't exists """
        if not os.path.exists(self.dest_path):
            os.mkdir(dest_path)

    def composeMDFilename(self):
        """ composes the name of the markdown file """
        name, _ = os.path.splitext(os.path.basename(self.rstPath))
        return os.path.join(self.dest_path, "%s.md"%name)

    def writeResultsOnFile(self, md_filename):
        """ write translation results on md_filename """
        md = open(md_filename, "w")
        md.write("---\n")
        for metaItem, metaVal in self.meta.iteritems():
            md.write("%s: %s\n"%(metaItem, metaVal))
        md.write("---\n\n")
        md.write(str(self.soup))
        md.close()

    def extractTitle(self):
        """ removes title from soup and returns it.
            It returns empty string when no title is found. """
        title = self.soup.find("h1")
        if title.has_key("class"):
            result = title.text.encode('utf-8')
            title.extract()
        else:
            result = ''
        return result

    def setCategory(self):
        """ sets the post category from meta list """
        for m in self.meta:
            if m.startswith("categories"):
                category = m.lstrip("categories:").strip()
                break
        else:
            category = ""
            print >> sys.stderr, "WARNING: no category defined in %s"%self.rstPath
        self.category = category

    def composeDestPathFromCategory(self, contentType):
        """ composes and returns the corresponding post path for the 
        given content type.
        Content types can be 'posts' or 'media' and define the paths
        for posts, and other resources (media) """
        if self.category == "":
            path = os.path.join(self.ruhohPath, contentType)
        else:
            path = os.path.join(self.ruhohPath, contentType, self.category)
        return path

####

#
#
#
#
#
#
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
    in a tuple: rstPath, ruhohPath """
    p = argparse.ArgumentParser(description="Converts from rst to ruhoh format", version="1.0")
    p.add_argument('paths', metavar='path', nargs='+', help="Source file path with .rst extension")
    p.add_argument("-d", "--draft", action="store_true", help="Mark converted file as draft", dest="draft")
    p.add_argument("-r", "--ruhohPath", action="store", help="Path to ruhoh local copy. Overrides config file specs.", dest="ruhohPath")
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
    if options.ruhohPath:
        ruhohPath = options.ruhohPath
    else:
        # check configuration file
        c = ConfigParser()
        try:
            c.read(CONF_FILENAME)
            ruhohPath = os.path.expanduser(c.get('RUHOH', 'local_path'))
        except:
            print >> sys.stderr, "Error: %s expected with contents\n"%CONF_FILENAME +\
                    "[RUHOH]\n" +\
                    "local_path = path/to/ruhoh/local/site"
            sys.exit(3)
    #
    if not os.path.exists(ruhohPath):
        print >> sys.stderr, "Error: file not found: %s"%ruhohPath
        sys.exit(5)
    #
    isDraft = options.draft
    #
    return sourcelist, ruhohPath, isDraft
#
def main():

    # try to set locale
    setLocale()

    # get configuration information
    sourcelist, ruhohPath, isDraft = checkParams()

    for rstPath in sourcelist:
        # prepare params for docutils
        sys.argv = [sys.argv[0], rstPath]

        # define html output filename for docutils
        html_file = tempfile.NamedTemporaryFile()
        htmlPath = html_file.name
        sys.argv.append(htmlPath)

        # generate html conversion
        description = ('Generates ruhoh\'s md documents from standalone '
                       'reStructuredText sources.  ' + default_description)
        publish_cmdline(writer_name='html', description=description)

        # create md for ruhoh
        translator = RST2RuhohTranslator(htmlPath, ruhohPath, rstPath, isDraft)
        translator.translate()
        translator.saveTranslation()
        #
    return 0
#
if __name__=="__main__":
    sys.exit(main())

