import argparse
from sys import stdin
from urllib.parse import quote
from urllib.request import Request, urlopen
from subprocess import run
from os import environ

api_dev_key = environ.get("PB_API_DEV_KEY")
api_user_key = environ.get("PB_API_USER_KEY") or None

expire_date_choices = ["N", "10M", "1H", "1D", "1W", "2W", "1M", "6M", '1Y']
formats = ["4cs", "6502acme", "6502kickass", "6502tasm", "abap", "actionscript", "actionscript3", "ada", "aimms",
           "algol68", "apache", "applescript", "apt_sources", "arduino", "arm", "asm", "asp", "asymptote", "autoconf",
           "autohotkey", "autoit", "avisynth", "awk", "bascomavr", "bash", "basic4gl", "dos", "bibtex", "blitzbasic",
           "b3d", "bmx", "bnf", "boo", "bf", "c", "c_winapi", "c_mac", "cil", "csharp", "cpp", "cpp-winapi", "cpp-qt",
           "c_loadrunner", "caddcl", "cadlisp", "ceylon", "cfdg", "chaiscript", "chapel", "clojure", "klonec",
           "klonecpp", "cmake", "cobol", "coffeescript", "cfm", "css", "cuesheet", "d", "dart", "dcl", "dcpu16", "dcs",
           "delphi", "oxygene", "diff", "div", "dot", "e", "ezt", "ecmascript", "eiffel", "email", "epc", "erlang",
           "euphoria", "fsharp", "falcon", "filemaker", "fo", "f1", "fortran", "freebasic", "freeswitch", "gambas",
           "gml", "gdb", "genero", "genie", "gettext", "go", "groovy", "gwbasic", "haskell", "haxe", "hicest",
           "hq9plus", "html4strict", "html5", "icon", "idl", "ini", "inno", "intercal", "io", "ispfpanel", "j", "java",
           "java5", "javascript", "jcl", "jquery", "json", "julia", "kixtart", "kotlin", "latex", "ldif", "lb", "lsl2",
           "lisp", "llvm", "locobasic", "logtalk", "lolcode", "lotusformulas", "lotusscript", "lscript", "lua", "m68k",
           "magiksf", "make", "mapbasic", "markdown", "matlab", "mirc", "mmix", "modula2", "modula3", "68000devpac",
           "mpasm", "mxml", "mysql", "nagios", "netrexx", "newlisp", "nginx", "nim", "text", "nsis", "oberon2",
           "objeck", "objc", "ocaml", "ocaml-brief", "octave", "oorexx", "pf", "glsl", "oobas", "oracle11", "oracle8",
           "oz", "parasail", "parigp", "pascal", "pawn", "pcre", "per", "perl", "perl6", "php", "php-brief", "pic16",
           "pike", "pixelbender", "pli", "plsql", "postgresql", "postscript", "povray", "powerbuilder", "powershell",
           "proftpd", "progress", "prolog", "properties", "providex", "puppet", "purebasic", "pycon", "python", "pys60",
           "q", "qbasic", "qml", "rsplus", "racket", "rails", "rbs", "rebol", "reg", "rexx", "robots", "rpmspec",
           "ruby", "gnuplot", "rust", "sas", "scala", "scheme", "scilab", "scl", "sdlbasic", "smalltalk", "smarty",
           "spark", "sparql", "sqf", "sql", "standardml", "stonescript", "sclang", "swift", "systemverilog", "tsql",
           "tcl", "teraterm", "thinbasic", "typoscript", "unicon", "uscript", "upc", "urbi", "vala", "vbnet",
           "vbscript", "vedit", "verilog", "vhdl", "vim", "visualprolog", "vb", "visualfoxpro", "whitespace", "whois",
           "winbatch", "xbasic", "xml", "xorg_conf", "xpp", "yaml", "z80", "zxbasic"]

parser = argparse.ArgumentParser(description='paste stdin to pastebin.com')
parser.add_argument('-n', '--name', dest='api_paste_name', metavar='NAME', help='title of paste',
                    default="Paste created with https://github.com/thepeshka/pb")
parser.add_argument('-pub', '--public', dest='api_paste_private', action='store_const',
                    const=0, default=1,
                    help='post public paste (default: unlisted)')
parser.add_argument('-s', '--silent', dest='silent', action='store_const',
                    const=True, default=False)

if api_user_key:
    parser.add_argument('-priv', '--private', dest='api_paste_private', action='store_const',
                        const=2, default=1,
                        help='post private paste (default: unlisted)')

parser.add_argument('-e', '--expires', dest='api_paste_expire_date', default='N', choices=expire_date_choices,
                    help="when paste should expire (default: N (never))")
parser.add_argument('-f', '--format', dest='api_paste_format', choices=formats)

if api_user_key:
    parser.add_argument('-a', '--anonymous', dest='anonymous', action='store_const', const=True, default=False,
                        help="create paste as guest")

args = parser.parse_args().__dict__

silent = args['silent']
del args['silent']

api_paste_code = ''
while True:
    try:
        chunk = stdin.read(1024)
    except KeyboardInterrupt:
        exit(0)
        break
    if not chunk:
        break
    api_paste_code = api_paste_code + chunk
    if not silent:
        print(chunk, end="")

args = dict(api_dev_key=api_dev_key, api_paste_code=api_paste_code, api_option="paste", **args)

if api_user_key:
    args.update({'api_user_key': api_user_key})
    if args['anonymous']:
        del args['api_user_key']
    del args['anonymous']

if not args['api_paste_format']:
    del args['api_paste_format']

encode = lambda s: quote(str(s), safe='')

args = dict(zip(map(encode, args.keys()), map(encode, args.values())))

args = '&'.join([k + "=" + args[k] for k in args])

response = urlopen(Request(
    'https://pastebin.com/api/api_post.php',
    method='POST',
    data=args.encode(),
    headers={"Content-Type": "application/x-www-form-urlencoded"}
)).read().decode()

if response.startswith('https://pastebin.com/'):
    print(response)
    try:
        run(['xclip', '-selection', 'clipboard'], input=response, encoding='ascii')
    except FileNotFoundError:
        pass
elif response.startswith('Bad API request, '):
    print(response.split(', '[1]))
    exit(1)
else:
    print(response)
