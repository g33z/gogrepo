import sys
import logging
import http.cookiejar as cookiejar
import html5lib

# lib mods
cookiejar.MozillaCookieJar.magic_re = r'.*'  # bypass the hardcoded "Netscape HTTP Cookie File" check

# filepath constants
GAME_STORAGE_DIR = r'.'
COOKIES_FILENAME = r'gog-cookies.dat'
MANIFEST_FILENAME = r'gog-manifest.dat'
SERIAL_FILENAME = r'!serial.txt'
INFO_FILENAME = r'!info.txt'

# configure logging
logFormatter = logging.Formatter("%(asctime)s | %(message)s", datefmt='%H:%M:%S')
rootLogger = logging.getLogger('ws')
rootLogger.setLevel(logging.DEBUG)
consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)

# logging aliases
info = rootLogger.info
warn = rootLogger.warning
debug = rootLogger.debug
error = rootLogger.error
log_exception = rootLogger.exception

treebuilder = html5lib.treebuilders.getTreeBuilder('etree')
parser = html5lib.HTMLParser(tree=treebuilder, namespaceHTMLElements=False)

# GOG URLs
GOG_HOME_URL = r'https://www.gog.com'
GOG_ACCOUNT_URL = r'https://www.gog.com/account'
GOG_LOGIN_URL = r'https://login.gog.com/login_check'

# GOG Constants
GOG_MEDIA_TYPE_GAME = '1'
GOG_MEDIA_TYPE_MOVIE = '2'

# HTTP request settings
HTTP_FETCH_DELAY = 1  # in seconds
HTTP_RETRY_DELAY = 5  # in seconds
HTTP_RETRY_COUNT = 3
HTTP_GAME_DOWNLOADER_THREADS = 4
HTTP_PERM_ERRORCODES = (404, 403, 503)

# Save manifest data for these os and lang combinations
DEFAULT_OS_LIST = ['windows']
DEFAULT_LANG_LIST = ['en']

# These file types don't have md5 data from GOG
SKIP_MD5_FILE_EXT = ['.txt', '.zip']

# Language table that maps two letter language to their unicode gogapi json name
LANG_TABLE = {'en': 'English',  # English
              'bl': '\u0431\u044a\u043b\u0433\u0430\u0440\u0441\u043a\u0438',  # Bulgarian
              'ru': '\u0440\u0443\u0441\u0441\u043a\u0438\u0439',  # Russian
              'gk': '\u0395\u03bb\u03bb\u03b7\u03bd\u03b9\u03ba\u03ac',  # Greek
              'sb': '\u0421\u0440\u043f\u0441\u043a\u0430',  # Serbian
              'ar': '\u0627\u0644\u0639\u0631\u0628\u064a\u0629',  # Arabic
              'br': 'Portugu\xeas do Brasil',  # Brazilian Portuguese
              'jp': '\u65e5\u672c\u8a9e',  # Japanese
              'ko': '\ud55c\uad6d\uc5b4',  # Korean
              'fr': 'fran\xe7ais',  # French
              'cn': '\u4e2d\u6587',  # Chinese
              'cz': '\u010desk\xfd',  # Czech
              'hu': 'magyar',  # Hungarian
              'pt': 'portugu\xeas',  # Portuguese
              'tr': 'T\xfcrk\xe7e',  # Turkish
              'sk': 'slovensk\xfd',  # Slovak
              'nl': 'nederlands',  # Dutch
              'ro': 'rom\xe2n\u0103',  # Romanian
              'es': 'espa\xf1ol',  # Spanish
              'pl': 'polski',  # Polish
              'it': 'italiano',  # Italian
              'de': 'Deutsch',  # German
              'da': 'Dansk',  # Danish
              'sv': 'svenska',  # Swedish
              'fi': 'Suomi',  # Finnish
              'no': 'norsk',  # Norsk
              }

VALID_OS_TYPES = ['windows', 'linux', 'mac']
VALID_LANG_TYPES = list(LANG_TABLE.keys())

ORPHAN_DIR_NAME = '!orphaned'
ORPHAN_DIR_EXCLUDE_LIST = [ORPHAN_DIR_NAME, '!misc']
ORPHAN_FILE_EXCLUDE_LIST = [INFO_FILENAME, SERIAL_FILENAME]
