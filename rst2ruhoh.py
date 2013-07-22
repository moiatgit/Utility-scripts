#! /usr/bin/env python
# encoding: utf-8

# This script takes a .rst file as first argument and converts it to a
# markdown with the same name and extension .md prepared for being
# used at ruhoh blogs

# required: docutils

# Generalities:
# - every rst file belongs to a collection.
# - the collection of a file is the name of the folder containing it
# - the collection structure is replicated on ruhoh destination
# - collection usually coincides with the meta information
#   'categories' but it is not a requirement.

# TODO: current version allows references to rst by simpy href to the
# corresponding .rst file.
# However it is limited to references in the same collection (folder).
# References to files at other categories are possible by using the
# ruhoh notation: '{{url}}/collection/permalink'.
# It should be possible to accept '../collection/rstfile' notation.
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
import urllib, urlparse
#
CONF_FILENAME = os.path.expanduser("~/.rst2ruhoh")  # configuration filename
#
class RST2RuhohTranslator:

    _SPECIAL_CHAR = {   # map for special character conversion
            ord(u'à'):u'a',
            ord(u'á'):u'a',
            ord(u'è'):u'e',
            ord(u'é'):u'e',
            ord(u'í'):u'i',
            ord(u'ï'):u'i',
            ord(u'ò'):u'o',
            ord(u'ó'):u'o',
            ord(u'ú'):u'u',
            ord(u'ü'):u'u',
            ord(u'ç'):u's',
            ord(u'ñ'):u'ny',
            ord(u'·'):None,
            ord(u' '):None
            }

    def __init__(self, htmlPath, ruhohPath, rstPath, isDraft):
        self.htmlPath  = htmlPath
        self.ruhohPath = ruhohPath
        self.rstPath   = os.path.realpath(rstPath)
        self.isDraft   = isDraft
        self.meta      = {} # includes the meta information of the file
        self.collection = os.path.basename(self.rstPath)
        self.dest_path = RST2RuhohTranslator.composePostDestinationPath(self.ruhohPath)
        self.path_media = RST2RuhohTranslator.composePostDestinationPath(self.ruhohPath)

    def translate(self):
        """ performs the translation from rst to ruhoh format. """
        self.setSoupFromHtml()
        self.setMetaInfo()
        self.setTitle()
        self.setCategories()
        self.setPermalink()
        self.setPostDate()
        self.setDraftOption()
        self.fixResourcePaths()

    def saveTranslation(self):
        """ saves the translation in the corresponding destination """
        self.createDestinationPathIfMissing()
        md_filename = RST2RuhohTranslator.composeMDFilename(self.dest_path, self.collection, self.rstPath)
        self.writeResultsOnFile(md_filename)

    @staticmethod
    def composePostDestinationPath(ruhohPath):
        """ (str) -> str

        composes and returns the destination path of the post
        """
        return os.path.join(ruhohPath, 'post')

    def composeMediaDestinationPath(ruhohPath):
        """ (str) -> str

        composes and returns the destination path of the media
        """
        return os.path.join(self.ruhohPath, 'media')

    def setTitle(self):
        """ (RST2RuhohTranslator) -> NoneType

        Sets the title of the post.  If there's no meta information
        for title, it includes this title as the meta title. 
        """
        title = self.extractTitle()
        if not title:
            title = 'untitled'
        self.addMetaIfMissing('title', title)
        self.title = title

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
                if self.collection == "":
                    img["src"]="{{urls.media}}/%s"%img["src"]
                else:
                    img["src"]="{{urls.media}}/%s/%s"%(self.collection, img["src"])
            else:
                print >> sys.stderr, "WARNING: file %s not found but linked"%img["src"]

    def fixRefPaths(self, path):
        """ fixes paths of references to other posts from given path
        ERROR
        The problem that I'm trying to resolve is:
        - up to now I always call rst2ruhoh from the directory
          containing the .rst to be converted. I've tried to be
          general in some places of this code but I've never tried.

        - sometimes I want to link from the rst to another rst. It can
          happen that the linked rst belongs to the same collection as
          the referee, but sometimes it could just belong to another
          collection.

        - sometimes I want to link to other resources (e.g. pdf) that
          could be on the same folder as the .rst but it could also be
          in another folder. By now I've been able to process properly
          just the case of the same folder.

        - sometimes I want just to link to an external resource.
          They're normaly pages in a website. I should'nt do anything
          special to these resources

        """
        for a in self.soup.findAll("a"):
            if a.has_key("href"):
                a["href"] = self.fixHRefPath(path, a["href"])

    def fixHRefPath(self, path, href):
        """ fixes href in the following way:
            1. if href points to an rst file, it tries to convert
            the link to its corresponding md file.
            2. if href points to an existing file, it copies the file
            to the {{urls.media}}/:collection/ folder and fixes
            consequently the path. Attention: in case the resource
            already exists it will be overriden without considering if
            they are differents nor if there are other md pointing at it.
            3. if href points to a non existing file within the
            filesystem, it issues a warning.
            4. if href points to an external file (e.g. http://) it
            keeps the link without changes.
        """
        if self.isExternalResource(href):
            return href

        fileref = os.path.join(path, href)
        if not os.path.exists(fileref):
            # href points to a non existing file within the filesystem:
            print >> sys.stderr, "WARNING: missing linked file %s"%href
            return "#"

        if href.endswith('.rst'):
            return self.convertRefToCorrespondingMD(fileref)

        # it is a reference to an existing resource
        return self.fixExistingResource(fileref, href)

    def convertRefToCorrespondingMD(self, fileref):
        """ (RST2RuhohTranslator, str) -> str

        Given an existing rst file, it finds out the corresponding
        permalink associated to this file.
        """
        filename = os.path.basename(fileref)
        collection = RST2RuhohTranslator.getCollectionFromPath(fileref)
        mdPath = RST2RuhohTranslator.composeMDFilename(self.dest_path, collection, filename)
        XXX vas per aquí: ara has de treure el titol del md si existeix.
        Ja està implementada la funció!
        després assegura't que neteges una mica el codi: hi ha funcions que ja no calen
        return "XXXunknown"

    @staticmethod
    def getCollectionFromPath(path):
        """ (str) -> str

        It returns the collection of the file at the given path.
        >>> RST2RuhohTranslator.getCollectionFromPath('../colname/filename')
        colname
        """
        return os.path.basename(os.path.dirname(path))

    @staticmethod
    def isExternalResource(resource):
        """ (str) -> bool

        Returns true if the resource corresponds to an external resource.

        It is considered an external resource if one of the following:
        1. "http[s]://"
        2. "ftp[s]"://"

        """
        return re.match("^(http)|(ftp)s?://", resource) <> None


    def fixExistingResource(self, fileref, href):
        """ fixes the path of an existing resource and returns it """
        if not os.path.exists(self.path_media):
            os.mkdir(self.path_media)
        shutil.copy(fileref, self.path_media)
        if self.collection == "":
            return "{{urls.media}}/%s"%href
        else:
            return "{{urls.media}}/%s/%s"%(self.collection, href)

    def fixRSTLink(self, rstlink):
        """ fixes anchor of a link to a rst file that might
        be or not already translated.
        It returns the fixed href value or, in case of error, '#' """
        if not os.path.exists(rstlink):
            print >> sys.stderr, "WARNING: missing linked file %s"%rstlink
        if '/' in rstlink:  # it includes path information
            collection = RST2RuhohTranslator.getCollectionFromPath(rstlink)
            rstname  = os.path.basename(rstlink)
            categorizedlink = os.path.join(collection, rstname)
            path = os.path.join(self.ruhohPath, 'posts', collection)
            mdlink = RST2RuhohTranslator.composeMDFilename(path, collection, rstname)
        else:
            collection = self.collection
            mdlink = RST2RuhohTranslator.composeMDFilename(self.dest_path, collection, rstlink)
        if not os.path.exists(mdlink):
            print >> sys.stderr, "WARNING: missing linked file %s"%mdlink
            return "#"
        linkedPermalink = self.extractPermalinkFromMD(mdlink)
        if linkedPermalink == "":
            linkedPermalink = "#"
            print >> sys.stderr, "WARNING: missing permalink tag in linked file %s"%mdlink
        else:
            name = RST2RuhohTranslator.getPermalinkName(linkedPermalink)
            linkedPermalink = self.composePermalinkFromCollectionAndName(collection, name)
        return linkedPermalink

    def setSoupFromHtml(self):
        """ sets soup from the html file """
        self.soup = RST2RuhohTranslator.getContentSoupFromFile(self.htmlPath)

    @staticmethod
    def getContentSoupFromFile(path):
        """ (str) -> BeautifulSoup

        It opens an existing file and returns the contents
        of the file as a BeautifulSoup
        """
        html = open(path).read()
        soup = BeautifulSoup(html)
        return soup.body.contents[1]    # cleaned up to body

    def setMetaInfo(self):
        """ processes all meta information included in soup and 
        includes it in the meta property """
        getComments = lambda text:isinstance(text, Comment)
        for comment in self.soup.findAll(text=getComments):
            c = str(comment).lstrip("<!--").rstrip("-->").strip()
            m = re.match("(\w+):(.+)", c)
            if m:  # is a setting
                metaItem  = m.group(1)
                metaValue = m.group(2).strip()
                self.meta[metaItem]=metaValue
                comment.extract()

    def createDestinationPathIfMissing(self):
        """ create collection folder if doesn't exists """
        if not os.path.exists(self.dest_path):
            os.mkdir(self.dest_path)

    @staticmethod
    def composeMDFilename(basePath, collection, rstFilename):
        """ (str, str, str) -> str

        composes the name of the markdown file from the base path,
        the collection and the rst file name"""
        name, _ = os.path.splitext(os.path.basename(rstFilename))
        return os.path.join(basePath, collection, "%s.md"%name)

    @staticmethod
    def extractPermalinkFromMD(mdpath):
        """ extracts and returns permalink information from the
        given md path. It returns empty string when permalink info
        is not present. """
        fd = open(mdpath)
        for lin in fd:
            m = re.match("^permalink: '(.*)'", lin)
            if m:
                permalink = m.group(1).strip()
                break
        else:
            permalink = ""
        fd.close()
        return permalink

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
        titleTag = RST2RuhohTranslator.getTitleItemFromSoup(self.soup)
        title = RST2RuhohTranslator.getTitleTextFromTag(titleTag)
        if titleTag:
            titleTag.extract()
        return title

    @staticmethod
    def getTitleItemFromSoup(soup):
        """ (BeautifulSoup) -> BeautifulSoup.Tag

        It finds and returns the title of the soup. It considers the 
        title of the soup as the contents within the first <h1> tag.
        It returns None if no title is found and issues a 
        warning
        """
        return soup.find("h1")

    @staticmethod
    def getTitleTextFromTag(tag):
        """ (BeautifulSoup.Tag) -> str

        It returns the text in unicode of a tag. If tag is None or
        there's no text at all, it returns "untitled" and issues
        a warning
        """
        if tag and tag.has_key("class"):
            title = tag.text.encode('utf-8')
        else:
            title = 'untitled'
            print >> sys.stderr, "WARNING: file %s not found but linked"%img["src"]
        return title


    def setCategories(self):
        """ (RST2RuhohTranslator) -> NoneType

        If categories is not present in meta, this function sets the
        collection of the rst file as the value for categories.
        """
        self.addMetaIfMissing('categories', self.collection)

    def setPermalink(self):
        """ (RST2RuhohTranslator) -> NoneType

        Creates the post permalink composed from title.

        (for back compatibility issues) if permalink is already
        specified at meta, this function issues a warning and ignores
        it.
        """
        if self.meta.has_key('permalink'):
            print >> sys.stderr, "WARNING: permalink information ignored at file %s"%self.rstPath

        permalink = RST2RuhohTranslator.composePermalink(self.collection, self.title)
        self.meta['permalink'] = permalink

    @staticmethod
    def composePermalink(collection, title):
        """ fixes the given original permalink by:
            1. granting it enclosed in quotations '
            2. granting it include collection
            3. in case original is empty, uses a normalized title
            collection and title must be nonempty strings
        """
        link = RST2RuhohTranslator.composePermalinkFromTitle(title)
        permalink = RST2RuhohTranslator.composePermalinkFromCollectionAndName(collection, link)
        return permalink

    @staticmethod
    def composePermalinkFromCollectionAndName(collection, name):
        """ composes and returns the permalink from the given collection
        and name. Result will be single-quoted.
        >>> RST2RuhohTranslator.composePermalinkFromCollectionAndName('cat','nam')
        "'/cat/nam'"
        """
        return "'/%s/%s'"%(collection, name)

    @staticmethod
    def getPermalinkName(original):
        """ from a permalink possibly enclosed in single quotes, and
        in the form of name | collection/name it extracts the name and
        returns it.
        >>> RST2RuhohTranslator.getPermalinkName("'simple_name'")
        simple_name
        >>> RST2RuhohTranslator.getPermalinkName("simple_name")
        simple_name
        >>> RST2RuhohTranslator.getPermalinkName("'/:collection/simple_name'")
        simple_name
        >>> RST2RuhohTranslator.getPermalinkName("'any/thing/simple_name'")
        simple_name
        """
        unquoted = RST2RuhohTranslator.removeSingleQuotations(original)
        name = os.path.basename(unquoted)
        return name

    @staticmethod
    def removeSingleQuotations(original):
        """ removes single quotations from the given original string
            if they're present
            >>> RST2RuhohTranslator.removeSingleQuotations("unquoted")
            "unquoted"
            >>> RST2RuhohTranslator.removeSingleQuotations("'quoted'")
            "quoted"
            >>> RST2RuhohTranslator.removeSingleQuotations("'uncorrectly quoted")
            "'uncorectly quoted"
        """
        m = re.match("'(.*)'", original)
        result = m.group(1) if m else original
        return result

    @staticmethod
    def composePermalinkFromTitle(title):
        """ (str) -> str

        It composes a permalink from the title of a post.

        It begins replacing special characters and
        then fixes it to be a proper url.

        """
        convert = RST2RuhohTranslator.replaceSpecialChar(title)
        urlsafe = url_fix(convert)
        return urlsafe

    @staticmethod
    def replaceSpecialChar(text):
        """ (str) -> str

        Replaces special characters from a text.
        It replaces each special character in _SPECIAL_CHAR keys
        by its corresponding ascii.
        """
        return text.lower()                                      \
                   .decode('utf8')                               \
                   .translate(RST2RuhohTranslator._SPECIAL_CHAR) \
                   .encode('ascii', 'ignore')

####


def url_fix(s, charset='utf-8'):
    """Sometimes you get an URL by a user that just isn't a real
    URL because it contains unsafe characters like ' ' and so on.  This
    function can fix some of the problems in a similar way browsers
    handle data entered by the user

    Found at https://github.com/mitsuhiko/werkzeug/blob/master/werkzeug/urls.py

    >>> url_fix(u'http://de.wikipedia.org/wiki/Elf (Begriffsklärung)')
    'http://de.wikipedia.org/wiki/Elf%20%28Begriffskl%C3%A4rung%29'

    :param charset: The target charset for the URL if the url was
                    given as unicode string.
    """
    if isinstance(s, unicode):
        s = s.encode(charset, 'ignore')
    scheme, netloc, path, qs, anchor = urlparse.urlsplit(s)
    path = urllib.quote(path, '/%')
    qs = urllib.quote_plus(qs, ':&=')
    return urlparse.urlunsplit((scheme, netloc, path, qs, anchor))

def setLocale():
    """ tries to set locale """
    try:
        import locale
        locale.setlocale(locale.LC_ALL, '')
    except:
        pass

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

