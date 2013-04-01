#!/bin/sh

# Author: Aaron Toponce
# Date: Mar 28, 2013
# License: Public Domain

### Edit only these variables as needed ###
URL="http://ae7.st/p/api" # $URL should point to the external API
AUTHOR="eightyeight"  # Your name as you want it to appear on the paste

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
    echo "--mmix, --modula2, --modula3, --mpasm, --mxml, --mysql, --newlisp,"
    echo "--nsis, --oberon2, --objc, --ocaml, --ocaml-brief, --oobas, --oracle11"
    echo "--oracle8, --oxygene, --oz, --pascal, --pcre, --per, --perl, --perl6,"
    echo "--pf, --php, --php-brief, --pic16, --pike, --pixelbender, --plaintext,"
    echo "--plsql, --postgresql, --povray, --powerbuilder, --powershell,"
    echo "--progress, --prolog, --properties, --providex, --purebasic, --python,"
    echo "--q, --qbasic, --rails, --rebol, --reg, --robots, --rpmspec, --rsplus,"
    echo "--ruby, --sas, --scala, --scheme, --scilab, --sdlbasic, --smalltalk,"
    echo "--smarty, --sql, --systemverilog, --tcl, --teraterm, --text,"
    echo "--thinbasic, --tsql, --typoscript, --unicon, --vala, --vb, --vbnet,"
    echo "--verilog, --vhdl, --vim, --visualfoxpro, --visualprolog, --whitespace,"
    echo "--whois, --winbatch, --xbasic, --xml, --xorg_conf, --xpp, --yaml, --z80"
    echo # blank line
    echo "Set lifetime. Default is no expiration."
    echo "-m, --minutes         Expire the post in 10 minutes."
    echo "-H, --hour            Expire the post in 1 hour."
    echo "-d, --day             Expire the post in 1 day."
    echo "-w, --week            Expire the post in 1 week."
    echo "-M, --month           Expire the post in 1 month (4 weeks)."
    echo "-y, --year            Expire the post in 1 year."
    echo # blank line
    echo "-p, --private         Create a private paste."
    echo "-r, --raw             Return the raw link without the HTML."
    echo "-h, --help            Print this usage summary and exit."
    echo # blank line
    echo "Examples:"
    echo # blank line
    echo "  pastebin /tmp/file.txt"
    echo "    Create a public paste with no highlighting or expiration."
    echo # blank line
    echo "  pastebin --c --private --day /tmp/file.txt"
    echo "    Create a private paste with C syntax highlighting that expires"
    echo "    in one day (24 hours)."
    echo # blank line
    echo "Originally created by Aaron Toponce <aaron.toponce@gmail.com>"
    echo "Released into the public domain."
    echo # blank line
}

function pastebin {
    while true; do
        case "$1" in
            --4cs) H="4cs"; shift;;
            --adap) H="adap"; shift;;
            --actionscript) H="actionscript"; shift;;
            --actionscript3) H="actionscript3"; shift;;
            --ada) H="ada"; shift;;
            --apache) H="apache"; shift;;
            --applescript) H="applescript"; shift;;
            --apt_sources) H="apt_sources"; shift;;
            --asm) H="asm"; shift;;
            --asp) H="asp"; shift;;
            --autoconf) H="autoconf"; shift;;
            --autohotkey) H="autohotkey"; shift;;
            --autoit) H="autoit"; shift;;
            --avisynth) H="avisynth"; shift;;
            --awk) H="awk"; shift;;
            --bash) H="bash"; shift;;
            --basic4gl) H="basic4gl"; shift;;
            --bf) H="bf"; shift;;
            --bibtex) H="bibtex"; shift;;
            --blitzbasic) H="blitzbasic"; shift;;
            --bnf) H="bnf"; shift;;
            --boo) H="boo"; shift;;
            --c) H="c"; shift;;
            --caddcl) H="caddcl"; shift;;
            --cadlisp) H="cadlisp"; shift;;
            --cfdg) H="cfdg"; shift;;
            --cfm) H="cfm"; shift;;
            --chaiscript) H="chaiscript"; shift;;
            --cil) H="cil"; shift;;
            --clojure) H="clojure"; shift;;
            --c_mac) H="c_mac"; shift;;
            --cmake) H="cmake"; shift;;
            --cobol) H="cobol"; shift;;
            --cpp) H="cpp"; shift;;
            --cpp-qt) H="cpp-qt"; shift;;
            --csharp) H="csharp"; shift;;
            --css) H="css"; shift;;
            --cuesheet) H="cuesheet"; shift;;
            --d) H="d"; shift;;
            --dcs) H="dcs"; shift;;
            --delphi) H="delphi"; shift;;
            --diff) H="diff"; shift;;
            --div) H="div"; shift;;
            --dos) H="dos"; shift;;
            --dot) H="dot"; shift;;
            --ecmascript) H="ecmascript"; shift;;
            --eiffel) H="eiffel"; shift;;
            --email) H="email"; shift;;
            --erlang) H="erlang"; shift;;
            --fo) H="fo"; shift;;
            --fortran) H="fortran"; shift;;
            --freebasic) H="freebasic"; shift;;
            --fsharp) H="fsharp"; shift;;
            --gambas) H="gambas"; shift;;
            --gdb) H="gdb"; shift;;
            --genero) H="genero"; shift;;
            --genie) H="genie"; shift;;
            --gettext) H="gettext"; shift;;
            --glsl) H="glsl"; shift;;
            --gml) H="gml"; shift;;
            --gnuplot) H="gnuplot"; shift;;
            --groovy) H="groovy"; shift;;
            --gwbasic) H="gwbasic"; shift;;
            --haskell) H="haskell"; shift;;
            --hicest) H="hicest"; shift;;
            --hq9plus) H="hq9plus"; shift;;
            --html4strict) H="html4strict"; shift;;
            --icon) H="icon"; shift;;
            --idl) H="idl"; shift;;
            --ini) H="ini"; shift;;
            --inno) H="inno"; shift;;
            --intercal) H="intercal"; shift;;
            --io) H="io"; shift;;
            --j) H="j"; shift;;
            --java) H="java"; shift;;
            --java5) H="java5"; shift;;
            --javascript) H="javascript"; shift;;
            --jquery) H="jquery"; shift;;
            --kixtart) H="kixtart"; shift;;
            --klonec) H="klonec"; shift;;
            --klonecpp) H="klonecpp"; shift;;
            --latex) H="latex"; shift;;
            --lisp) H="lisp"; shift;;
            --locobasic) H="locobasic"; shift;;
            --logtalk) H="logtalk"; shift;;
            --lolcode) H="lolcode"; shift;;
            --lotusformulas) H="lotusformulas"; shift;;
            --lotusscript) H="lotusscript"; shift;;
            --lscript) H="lscript"; shift;;
            --lsl2) H="lsl2"; shift;;
            --lua) H="lua"; shift;;
            --m68k) H="m68k"; shift;;
            --magiksf) H="magiksf"; shift;;
            --make) H="make"; shift;;
            --mapbasic) H="mapbasic"; shift;;
            --matlab) H="matlab"; shift;;
            --mirc) H="mirc"; shift;;
            --mmix) H="mmix"; shift;;
            --modula2) H="modula2"; shift;;
            --modula3) H="modula3"; shift;;
            --mpasm) H="mpasm"; shift;;
            --mxml) H="mxml"; shift;;
            --mysql) H="mysql"; shift;;
            --newlisp) H="newlisp"; shift;;
            --nsis) H="nsis"; shift;;
            --oberon2) H="oberon2"; shift;;
            --objc) H="objc"; shift;;
            --ocaml) H="ocaml"; shift;;
            --ocaml-brief) H="ocaml-brief"; shift;;
            --oobas) H="oobas"; shift;;
            --oracle11) H="oracle11"; shift;;
            --oracle8) H="oracle8"; shift;;
            --oxygene) H="oxygene"; shift;;
            --oz) H="oz"; shift;;
            --pascal) H="pascal"; shift;;
            --pcre) H="pcre"; shift;;
            --per) H="per"; shift;;
            --perl) H="perl"; shift;;
            --perl6) H="perl6"; shift;;
            --pf) H="pf"; shift;;
            --php) H="php"; shift;;
            --php-brief) H="php-brief"; shift;;
            --pic16) H="pic16"; shift;;
            --pike) H="pike"; shift;;
            --pixelbender) H="pixelbender"; shift;;
            --plaintext) H="plaintext"; shift;;
            --plsql) H="plsql"; shift;;
            --postgresql) H="postgresql"; shift;;
            --povray) H="povray"; shift;;
            --powerbuilder) H="powerbuilder"; shift;;
            --powershell) H="powershell"; shift;;
            --progress) H="progress"; shift;;
            --prolog) H="prolog"; shift;;
            --properties) H="properties"; shift;;
            --providex) H="providex"; shift;;
            --purebasic) H="purebasic"; shift;;
            --python) H="python"; shift;;
            --q) H="q"; shift;;
            --qbasic) H="qbasic"; shift;;
            --rails) H="rails"; shift;;
            --rebol) H="rebol"; shift;;
            --reg) H="reg"; shift;;
            --robots) H="robots"; shift;;
            --rpmspec) H="rpmspec"; shift;;
            --rsplus) H="rsplus"; shift;;
            --ruby) H="ruby"; shift;;
            --sas) H="sas"; shift;;
            --scala) H="scala"; shift;;
            --scheme) H="scheme"; shift;;
            --scilab) H="scilab"; shift;;
            --sdlbasic) H="sdlbasic"; shift;;
            --smalltalk) H="smalltalk"; shift;;
            --smarty) H="smarty"; shift;;
            --sql) H="sql"; shift;;
            --systemverilog) H="systemverilog"; shift;;
            --tcl) H="tcl"; shift;;
            --teraterm) H="teraterm"; shift;;
            --text) H="text"; shift;;
            --thinbasic) H="thinbasic"; shift;;
            --tsql) H="tsql"; shift;;
            --typoscript) H="typoscript"; shift;;
            --unicon) H="unicon"; shift;;
            --vala) H="vala"; shift;;
            --vb) H="vb"; shift;;
            --vbnet) H="vbnet"; shift;;
            --verilog) H="verilog"; shift;;
            --vhdl) H="vhdl"; shift;;
            --vim) H="vim"; shift;;
            --visualfoxpro) H="visualfoxpro"; shift;;
            --visualprolog) H="visualprolog"; shift;;
            --whitespace) H="whitespace"; shift;;
            --whois) H="whois"; shift;;
            --winbatch) H="winbatch"; shift;;
            --xbasic) H="xbasic"; shift;;
            --xml) H="xml"; shift;;
            --xorg_conf) H="xorg_conf"; shift;;
            --xpp) H="xpp"; shift;;
            --yaml) H="yaml"; shift;;
            --z80) H="z80"; shift;;
            -p|--private) P="private"; shift;;
            -m|--minutes) L="1"; shift;;
            -H|--hour) L="2"; shift;;
            -d|--day) L="3"; shift;;
            -w|--week) L="4"; shift;;
            -M|--month) L="5"; shift;;
            -y|--year) L="6"; shift;;
            -r|--raw) R="raw"; shift;;
            -h|--help) usage; exit 0;;
            *)
                # if $1 is a file on the filesystem
                if [ -e $1 ]; then
                    # curl(1) interprets special characters in the source file
                    # conert those to unicode equivalents
                    cat $1 > /tmp/pastebin.tmp
                    sed -ir 's# #%20#g' /tmp/pastebin.tmp           # space
                    sed -ir 's#"#%22#g' /tmp/pastebin.tmp           # "
                    sed -ir "s#'#%27#g" /tmp/pastebin.tmp           # '
                    sed -ir 's#`#%60#g' /tmp/pastebin.tmp           # `
                    sed -ir 's#\\#%5c#g' /tmp/pastebin.tmp          # \
                    sed -ir 's#&%20#26%20#g' /tmp/pastebin.tmp      # &space;
                    sed -ir 's#%20&#%2026#g' /tmp/pastebin.tmp      # space&
                    sed -ir 's#@#%40#g' /tmp/pastebin.tmp           # @
                    sed -ir 's#-#%2d#g' /tmp/pastebin.tmp           # -
                    sed -ir 's#=%20#%3d%20#g' /tmp/pastebin.tmp     # =space
                    sed -ir 's#%20=#%20%3d#g' /tmp/pastebin.tmp     # space=
                    TEXT=$(cat /tmp/pastebin.tmp)
                    rm /tmp/pastebin.tmp
                    break
                else
                    printf "Invalid option: $1\n\n"
                    usage
                    exit 1
                fi
                ;;
        esac
    done

    if [ -z $H ]; then H="plaintext"; fi    # <select name=highlighter>
    if [ -z $P ]; then P="public"; fi       # <select name=privacy>
    if [ -z $L ]; then L="0"; fi            # <select name=lifespan>

    LINK=$(curl -d author="$AUTHOR" -d pasteEnter="$TEXT" -d highlighter="$H"\
        -d privacy="$P" -d lifespan="$L" $URL 2> /dev/null |\
        awk -F '"' '/url/ {print $4}')

    if [ ! -z "$R" ]; then
        LINK="${LINK}@raw"
    fi

    echo $LINK
}
