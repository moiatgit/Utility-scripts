# more natural completion of cd with environment variables
# Usage:
#   Source this file, for example in your ~/.bashrc or similar. e.g.
#   source cd_completion.sh
#
_cd_completion() {
    local cur="${COMP_WORDS[COMP_CWORD]}"
    local prefix

    # Returns a list of environment variables starting with the prefix
    get_env_vars() {
        local prefix="$1"
        readarray -t COMPREPLY < <(compgen -v "$prefix")

        # Filter results to only include directories
        local results=()
        for var in "${COMPREPLY[@]}"; do
            if [[ -d "${!var}" ]]; then
                results+=("\$$var")
            fi
        done
        COMPREPLY=("${results[@]}")
    }

    if [[ "$cur" == \$* && "$cur" != *\/ ]]; then
        # Get environment variables starting with the prefix
        prefix=${cur:1}
        get_env_vars "$prefix"
    elif [[ "$cur" == \$*\/ ]]; then
        # Get the value of the environment variable and append a slash
        prefix="${cur%/}"
        prefix=${prefix:1}
        COMPREPLY="${!prefix}"/
    else
        # Get directories
        readarray -t COMPREPLY < <(compgen -d -- "$cur")
        for i in "${!COMPREPLY[@]}"; do
            COMPREPLY[$i]="${COMPREPLY[$i]%/}/"
        done
    fi

    # Add nospace option if there is only one completion option
    if [[ ${#COMPREPLY[@]} -eq 1 ]]; then
        compopt -o nospace
    fi
}
complete -F '_cd_completion' cd
