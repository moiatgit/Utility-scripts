# process killer with a nice effect
# Usage: kill a process by name
# $ bye program
#
# Source this file in your .barhrc or similar
function flip() {
  perl -C3 -Mutf8 -lpe '$_=reverse;y/a-zA-Z.['\'',({?!\"<_;‿⁅∴\r/ɐqɔpǝɟƃɥıɾʞ|ɯuodbɹsʇnʌʍxʎzɐqɔpǝɟƃɥıɾʞ|ɯuodbɹsʇnʌʍxʎz˙],'\'')}¿¡,>‾؛⁀⁆∵\n/' <<< "$1"
}
function bye() {
    for target in $*
    do
        pkill -9 $target && echo -e "\n   « $(flip $target) »\n"
    done
}

