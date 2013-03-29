#!/bin/zsh

# Author: Aaron Toponce
# Date: Mar 28, 2013
# License: Public Domain

### Edit only these variables as needed ###
URL="http://paste.example.com/api" # $URL should point to the external API

### DO NOT EDIT BELOW HERE ###
function usage {
    echo "usage: pastebin [OPTION]... FILE"
    echo "Creates a pastebin using the Knoxious Pastebin API."
    echo # blank line
    echo "The following languages are supported for syntax highlighting:"
    echo "--4cs, --abap, --actionscript, --actionscript3, --ada, --apache,"
    echo "--applescript, --apt_sources, --asm, --asp, --autoconf, --autohotkey,"
    echo "--autoit, --avisynth, --awk, --bash, --basic4gl, --bf, --bibtex,"
    echo "--blitzbasic, --bnf, --boo, --c, --caddcl, --cadlisp, --cfdg, --cfm,"
    echo "--chaiscript, --cil, --clojure, --c_mac, --cmake, --cobol, --cpp,"
    echo "--cpp-qt, --csharp, --css, --cuesheet, --d, --dcs, --delphi, --diff,"
    echo "--div, --dos, --dot, --ecmascript, --eiffel, --email, --erlang, --fo,"
    echo "--fortran, --freebasic, --fsharp, --gambas, --gdb, --genero, --genie,"
    echo "--gettext, --glsl, --gml, --gnuplot, --groovy, --gwbasic, --haskell,"
    echo "--hicest, --hq9plus, --html4strict, --icon, --idl, --ini, --inno,"
    echo "--intercal, --io, --j, --java, --java5, --javascript, --jquery,"
    echo "--kixtart, --klonec, --klonecpp, --latex, --lisp, --locobasic,"
    echo "--logtalk, --lolcode, --lotusformulas, --lotusscript, --lscript,"
    echo "--lsl2, --lua, --m68k, --magiksf, --make, --mapbasic, --matlab, --mirc,"
    echo "--mmix, --modula2, --modula3 --mpasm, --mxml, --mysql, --newlisp,"
    echo "--nsis, --oberon2 --objc, --ocaml, --ocaml-brief, --oobas, --oracle11"
    echo "--oracle8, --oxygene, --oz, --pascal, --pcre, --per, --perl, --perl6,"
    echo "--pf, --php, --php-brief, --pic16 --pike, --pixelbender, --plaintext,"
    echo "--plsql, --postgresql, --povray, --powerbuilder, --powershell,"
    echo "--progress, --prolog, --properties, --providex, --purebasic, --python,"
    echo "--q, --qbasic, --rails, --rebol, --reg, --robots, --rpmspec, --rsplus,"
    echo "--ruby, --sas, --scala, --scheme, --scilab, --sdlbasic, --smalltalk,"
    echo "--smarty, --sql, --systemverilog, --tcl, --teraterm, --text,"
    echo "--thinbasic, --tsql, --typoscript, --unicon, --vala, --vb, --vbnet,"
    echo "--verilog, --vhdl, --vim, --visualfoxpro, --visualprolog, --whitespace,"
    echo "--whois, --winbatch, --xbasic, --xml, --xorg_conf, --xpp, --yaml, --z80"
    echo # blank line
    echo "--public          Create a public paste."
    echo "--private         Create a private paste."
    echo # blank line
    echo "--minutes         Expire the post in 10 minutes."
    echo "--hour            Expire the post in 1 hour."
    echo "--day             Expire the post in 1 day."
    echo "--week            Expire the post in 1 week."
    echo "--month           Expire the post in 1 month (4 weeks)."
    echo "--year            Expire the post in 1 year."
    echo # blank line
    echo "-h, --help        Print this usage summary and exit."
    echo # blank line
    echo "Examples:"
    echo # blank line
    echo "  pastebin /tmp/file.txt"
    echo "    Create a public paste that with no highlighting or expiration."
    echo # blank line
    echo "  pastebin --c --private --day /tmp/file.txt"
    echo "    Create a private paste with C syntax highlighting that expires"
    echo "    in one day (24 hours)."
    echo # blank line
    echo "Originally created by Aaron Toponce <aaron.toponce@gmail.com>"
    echo "Released into the public domain."
    echo # blank line
}

autoload -U colors && colors

TEMP=$(getopt -o h -l 4cs,abap,actionscript,actionscript3,ada,apache,\
applescript,apt_sources,asm,asp,autoconf,autohotkey,autoit,avisynth,awk,bash,\
basic4gl,bf,bibtex,blitzbasic,bnf,boo,c,caddcl,cadlisp,cfdg,cfm,chaiscript,\
cil,clojure,c_mac,cmake,cobol,cpp,cpp-qt,csharp,css,cuesheet,d,dcs,delphi,\
diff,div,dos,dot,ecmascript,eiffel,email,erlang,fo,fortran,freebasic,fsharp,\
gambas,gdb,genero,genie,gettext,glsl,gml,gnuplot,groovy,gwbasic,haskell,\
hicest,hq9plus,html4strict,icon,idl,ini,inno,intercal,io,j,java,java5,\
javascript,jquery,kixtart,klonec,klonecpp,latex,lisp,locobasic,logtalk,\
lolcode,lotusformulas,lotusscript,lscript,lsl2,lua,m68k,magiksf,make,\
mapbasic,matlab,mirc,mmix,modula2,modula3mpasm,mxml,mysql,newlisp,nsis,\
oberon2objc,ocaml,ocaml-brief,oobas,oracle11oracle8,oxygene,oz,pascal,pcre,\
per,perl,perl6,pf,php,php-brief,pic16pike,pixelbender,plaintext,plsql,\
postgresql,povray,powerbuilder,powershell,progress,prolog,properties,\
providex,purebasic,python,q,qbasic,rails,rebol,reg,robots,rpmspec,rsplus,ruby,\
sas,scala,scheme,scilab,sdlbasic,smalltalk,smarty,sql,systemverilog,tcl,\
teraterm,text,thinbasic,tsql,typoscript,unicon,vala,vb,vbnet,verilog,vhdl,vim,\
visualfoxpro,visualprolog,whitespace,whois,winbatch,xbasic,xml,xorg_conf,xpp,\
yaml,z80,public,private,minutes,hour,day,week,month,year,help -n $0 -- "$@")
if [ $? != 0 ]; then echo "Internal error..." >&2; exit 1; fi

eval set -- "$TEMP"
while true; do
    case "$1" in
        --4cs) L="4cs"; shift;;
        --adap) L="adap"; shift;;
        --actionscript) L="actionscript"; shift;;
        --actionscript3) L="actionscript3"; shift;;
        --ada) L="ada"; shift;;
        --apache) L="apache"; shift;;
        --applescript) L="applescript"; shift;;
        --apt_sources) L="apt_sources"; shift;;
        --asm) L="asm"; shift;;
        --asp) L="asp"; shift;;
        --autoconf) L="autoconf"; shift;;
        --autohotkey) L="autohotkey"; shift;;
        --autoit) L="autoit"; shift;;
        --avisynth) L="avisynth"; shift;;
        --awk) L="awk"; shift;;
        --bash) L="bash"; shift;;
        --basic4gl) L="basic4gl"; shift;;
        --bf) L="bf"; shift;;
        --bibtex) L="bibtex"; shift;;
        --blitzbasic) L="blitzbasic"; shift;;
        --bnf) L="bnf"; shift;;
        --boo) L="boo"; shift;;
        --c) L="c"; shift;;
        --caddcl) L="caddcl"; shift;;
        --cadlisp) L="cadlisp"; shift;;
        --cfdg) L="cfdg"; shift;;
        --cfm) L="cfm"; shift;;
        --chaiscript) L="chaiscript"; shift;;
        --cil) L="cil"; shift;;
        --clojure) L="clojure"; shift;;
        --c_mac) L="c_mac"; shift;;
        --cmake) L="cmake"; shift;;
        --cobol) L="cobol"; shift;;
        --cpp) L="cpp"; shift;;
        --cpp-qt) L="cpp-qt"; shift;;
        --csharp) L="csharp"; shift;;
        --css) L="css"; shift;;
        --cuesheet) L="cuesheet"; shift;;
        --d) L="d"; shift;;
        --dcs) L="dcs"; shift;;
        --delphi) L="delphi"; shift;;
        --diff) L="diff"; shift;;
        --div) L="div"; shift;;
        --dos) L="dos"; shift;;
        --dot) L="dot"; shift;;
        --ecmascript) L="ecmascript"; shift;;
        --eiffel) L="eiffel"; shift;;
        --email) L="email"; shift;;
        --erlang) L="erlang"; shift;;
        --fo) L="fo"; shift;;
        --fortran) L="fortran"; shift;;
        --freebasic) L="freebasic"; shift;;
        --fsharp) L="fsharp"; shift;;
        --gambas) L="gambas"; shift;;
        --gdb) L="gdb"; shift;;
        --genero) L="genero"; shift;;
        --genie) L="genie"; shift;;
        --gettext) L="gettext"; shift;;
        --glsl) L="glsl"; shift;;
        --gml) L="gml"; shift;;
        --gnuplot) L="gnuplot"; shift;;
        --groovy) L="groovy"; shift;;
        --gwbasic) L="gwbasic"; shift;;
        --haskell) L="haskell"; shift;;
        --hicest) L="hicest"; shift;;
        --hq9plus) L="hq9plus"; shift;;
        --html4strict) L="html4strict"; shift;;
        --icon) L="icon"; shift;;
        --idl) L="idl"; shift;;
        --ini) L="ini"; shift;;
        --inno) L="inno"; shift;;
        --intercal) L="intercal"; shift;;
        --io) L="io"; shift;;
        --j) L="j"; shift;;
        --java) L="java"; shift;;
        --java5) L="java5"; shift;;
        --javascript) L="javascript"; shift;;
        --jquery) L="jquery"; shift;;
        --kixtart) L="kixtart"; shift;;
        --klonec) L="klonec"; shift;;
        --klonecpp) L="klonecpp"; shift;;
        --latex) L="latex"; shift;;
        --lisp) L="lisp"; shift;;
        --locobasic) L="locobasic"; shift;;
        --logtalk) L="logtalk"; shift;;
        --lolcode) L="lolcode"; shift;;
        --lotusformulas) L="lotusformulas"; shift;;
        --lotusscript) L="lotusscript"; shift;;
        --lscript) L="lscript"; shift;;
        --lsl2) L="lsl2"; shift;;
        --lua) L="lua"; shift;;
        --m68k) L="m68k"; shift;;
        --magiksf) L="magiksf"; shift;;
        --make) L="make"; shift;;
        --mapbasic) L="mapbasic"; shift;;
        --matlab) L="matlab"; shift;;
        --mirc) L="mirc"; shift;;
        --mmix) L="mmix"; shift;;
        --modula2) L="modula2"; shift;;
        --modula3mpasm) L="modula3mpasm"; shift;;
        --mxml) L="mxml"; shift;;
        --mysql) L="mysql"; shift;;
        --newlisp) L="newlisp"; shift;;
        --nsis) L="nsis"; shift;;
        --oberon2objc) L="oberon2objc"; shift;;
        --ocaml) L="ocaml"; shift;;
        --ocaml-brief) L="ocaml-brief"; shift;;
        --oobas) L="oobas"; shift;;
        --oracle11oracle8) L="oracle11oracle8"; shift;;
        --oxygene) L="oxygene"; shift;;
        --oz) L="oz"; shift;;
        --pascal) L="pascal"; shift;;
        --pcre) L="pcre"; shift;;
        --per) L="per"; shift;;
        --perl) L="perl"; shift;;
        --perl6) L="perl6"; shift;;
        --pf) L="pf"; shift;;
        --php) L="php"; shift;;
        --php-brief) L="php-brief"; shift;;
        --pic16pike) L="pic16pike"; shift;;
        --pixelbender) L="pixelbender"; shift;;
        --plaintext) L="plaintext"; shift;;
        --plsql) L="plsql"; shift;;
        --postgresql) L="postgresql"; shift;;
        --povray) L="povray"; shift;;
        --powerbuilder) L="powerbuilder"; shift;;
        --powershell) L="powershell"; shift;;
        --progress) L="progress"; shift;;
        --prolog) L="prolog"; shift;;
        --properties) L="properties"; shift;;
        --providex) L="providex"; shift;;
        --purebasic) L="purebasic"; shift;;
        --python) L="python"; shift;;
        --q) L="q"; shift;;
        --qbasic) L="qbasic"; shift;;
        --rails) L="rails"; shift;;
        --rebol) L="rebol"; shift;;
        --reg) L="reg"; shift;;
        --robots) L="robots"; shift;;
        --rpmspec) L="rpmspec"; shift;;
        --rsplus) L="rsplus"; shift;;
        --ruby) L="ruby"; shift;;
        --sas) L="sas"; shift;;
        --scala) L="scala"; shift;;
        --scheme) L="scheme"; shift;;
        --scilab) L="scilab"; shift;;
        --sdlbasic) L="sdlbasic"; shift;;
        --smalltalk) L="smalltalk"; shift;;
        --smarty) L="smarty"; shift;;
        --sql) L="sql"; shift;;
        --systemverilog) L="systemverilog"; shift;;
        --tcl) L="tcl"; shift;;
        --teraterm) L="teraterm"; shift;;
        --text) L="text"; shift;;
        --thinbasic) L="thinbasic"; shift;;
        --tsql) L="tsql"; shift;;
        --typoscript) L="typoscript"; shift;;
        --unicon) L="unicon"; shift;;
        --vala) L="vala"; shift;;
        --vb) L="vb"; shift;;
        --vbnet) L="vbnet"; shift;;
        --verilog) L="verilog"; shift;;
        --vhdl) L="vhdl"; shift;;
        --vim) L="vim"; shift;;
        --visualfoxpro) L="visualfoxpro"; shift;;
        --visualprolog) L="visualprolog"; shift;;
        --whitespace) L="whitespace"; shift;;
        --whois) L="whois"; shift;;
        --winbatch) L="winbatch"; shift;;
        --xbasic) L="xbasic"; shift;;
        --xml) L="xml"; shift;;
        --xorg_conf) L="xorg_conf"; shift;;
        --xpp) L="xpp"; shift;;
        --yaml) L="yaml"; shift;;
        --z80) L="z80"; shift;;
        --public) P="public"; shift;;
        --private) P="private"; shift;;
        --minutes) E="1"; shift;;
        --hour) E="2"; shift;;
        --day) E="3"; shift;;
        --week) E="4"; shift;;
        --month) E="5"; shift;;
        --year) E="6"; shift;;
        -h|--help) usage; exit 0;;
        *)
            if [ -e $1 ]; then
                TEXT="$(cat $1)"
                echo $TEXT
            else
                printf "$fg[red]invalid option:$reset_color $1\n\n"
                usage
                exit 1
            fi
            ;;
    esac
done

if [ -z $L ]; then L="plaintext"; fi    # <select name=highlighter>
if [ -z $P ]; then P="public"; fi       # <select name=privacy>
if [ -z $E ]; then E="0"; fi            # <select name=lifespan>

#curl -d author=eightyeight -d pasteEnter="$TEXT" $URL |\
#awk -F '"' '/url/ {print $4}'
