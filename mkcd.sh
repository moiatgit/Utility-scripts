# function to mk + cd on a directory
# It creates parents if needed
# It will simply cd when already exists
# It depends on _cd_completion
#
# Usage:
# source this file after sourcing cd_completion.sh. e.g. in your .basrc
function mkcd() {
  [ -n "$1" ] && mkdir -p "$@" && cd "$1";
}

#complete -F '_cd_completion' mkcd
