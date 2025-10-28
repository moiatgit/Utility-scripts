#! /bin/bash
echo "Sets the ~/.Xmodmap file to remap cat keys"
if [[ "$1" == "go" ]];
then
    xmodmap -e "keycode  13 = 4 dollar 4 dollar asciitilde EuroSign 4 dollar"
    xmodmap -e "keycode  21 = exclamdown questiondown equal plus EuroSign EuroSign equal plus"
    xmodmap -e "keycode  38 = a A a A agrave Agrave"
    xmodmap -e "keycode  24 = q Q q Q aacute Aacute q Q"
    xmodmap -e "keycode  26 = e E e E eacute Eacute e E"
    xmodmap -e "keycode  40 = d D d D egrave Egrave d D"
    xmodmap -e "keycode  30 = u U u U uacute Uacute u U"
    xmodmap -e "keycode  31 = i I i I iacute Iacute i I"
    xmodmap -e "keycode  32 = o O o O oacute Oacute o O"
    xmodmap -e "keycode  44 = j J j J udiaeresis Udiaeresis j J"
    xmodmap -e "keycode  45 = k K k K Idiaeresis Idiaeresis k K"
    xmodmap -e "keycode  46 = l L l L ograve Ograve l L"
    xmodmap -e "keycode  54 = c C c C ccedilla Ccedilla c C"
    xmodmap -e "keycode  57 = n N n N ntilde Ntilde n N"
    xmodmap -e "keycode  52 = z Z z Z less guillemotleft z Z"
    xmodmap -e "keycode  53 = x X x X greater guillemotright x X"
    xmodmap -e "keycode  34 = asciicircum grave bracketleft braceleft bracketleft dead_abovering bracketleft braceleft"
elif [[ "$1" == "recover" ]];
then
    xmodmap -e "keycode  21 = exclamdown questiondown equal plus dead_tilde asciitilde equal plus"
    xmodmap -e "keycode  24 = q Q q Q at Greek_OMEGA q Q"
    xmodmap -e "keycode  38 = a A a A ae AE a A"
    xmodmap -e "keycode  26 = e E e E EuroSign cent e E"
    xmodmap -e "keycode  40 = d D d D eth ETH d D"
    xmodmap -e "keycode  30 = u U u U downarrow uparrow u U"
    xmodmap -e "keycode  31 = i I i I rightarrow idotless i I"
    xmodmap -e "keycode  32 = o O o O oslash Oslash o O"
    xmodmap -e "keycode  44 = j J j J dead_hook dead_horn j J"
    xmodmap -e "keycode  45 = k K k K kra ampersand k K"
    xmodmap -e "keycode  46 = l L l L U0140 U013F l L"
    xmodmap -e "keycode  54 = c C c C cent copyright c C"
    xmodmap -e "keycode  57 = n N n N n N n N"
    xmodmap -e "keycode  52 = z Z z Z guillemotleft less z Z"
    xmodmap -e "keycode  53 = x X x X guillemotright greater x X"
    xmodmap -e "keycode  13 = 4 dollar 4 dollar asciitilde dollar 4 dollar"
    xmodmap -e "keycode  34 = dead_grave dead_circumflex bracketleft braceleft bracketleft dead_abovering bracketleft braceleft"

else
    echo "go: actually sets the mappings. recover: recover default layout"
fi


