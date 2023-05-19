# more natural completion of cd with environment variables
# Usage:
#   Source this file, for example in your ~/.bashrc or similar. e.g.
#   source cd_completion.sh
#
#   TODO: consider accepting ~/ paths without escaping the ~

##################
# Helper functions
##################

# Return the starting environment variable from the string in $1
extract_env_var() {
    if [[ "$1" == *"$"* ]]; then
        echo "$1" | grep -o '$[a-zA-Z_][a-zA-Z_0-9]*'
    else
        echo ""
    fi
}

# Returns the contents after an starting environment variable
extract_rest() {
    echo "${1#*/}"
}

# Returns a list of environment variables starting with the prefix
get_folder_envars() {
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

# extracts the relative path of $1 from $2
get_relative_path() {
    v1="$1"
    v2="$2"

    # Remove trailing slash from v2
    v2="${v2%/}"

    # If v2 is not a prefix of v1, return an empty string
    if [[ "$v1" != "$v2"* ]]; then
        echo ""
        return
    fi

    # Remove v2 from the beginning of v1 and return the result
    echo "${v1#$v2/}"
}

# Returns the corresponding value of a environment variable whose name is in $1
expand_env_var() {
    # Get the value of the environment variable and append a slash
    prefix="${1%/}"
    prefix=${prefix:1}
    echo "${!prefix}"
}


######################
# completion functions
######################

_file_completion() {
    local cur="${COMP_WORDS[COMP_CWORD]}"
    local envar_name=$(extract_env_var "$cur")
    local cmd="${COMP_WORDS[0]}"
    if [[ "$envar_name" == "" && "$cur" != '$' ]]; then   # completion without environment variable
        readarray -t COMPREPLY < <(compgen -f -- "$cur")
    else
        if [[ "$envar_name" == "$cur" || "$cur" == '$' ]]; then   # not yet completed environment var
            # Get environment variables starting with the prefix
            local prefix=${cur:1}
            get_folder_envars "$prefix"
        else                        # environment var is already completed
            local rest=$(extract_rest "$cur")
            local expanded=$(expand_env_var "$envar_name")
            local complete="$expanded/$rest"
            readarray -t COMPREPLY < <(compgen -f -- "$cur")
        fi
    fi

    # potst process the results
    # 1. append / to the results that correspond to a folder
    # 2. escape special characters
    local results=()
    for var in "${COMPREPLY[@]}"; do
        local envar_name=$(extract_env_var "$var")
        # local to_check="$var"
        local to_check="$var"
        local to_append=''
        if [[ "$envar_name" != "" ]]; then
            expanded=$(expand_env_var "$envar_name")
            rest=$(extract_rest "$var/")
            if [[ "$rest" != "" ]]; then
                escaped="$(printf "%q" "$rest")"     # escape special chars like whitespace
                to_check="$expanded/$rest"
                to_append="$envar_name/$escaped"
            else
                to_check="$expanded"
                to_append="$envar_name"
            fi
        else
            to_append="$(printf "%q" "$var")"
        fi
        if [[ -d "${to_check}" ]]; then
            results+=("$to_append/")
        elif [[ -f "${to_check}" ]]; then
            results+=("$to_append ")
        else
            results+=("$to_append")
        fi
    done
    COMPREPLY=("${results[@]}")

    # Add nospace option if there is only one completion option
    if [[ ${#COMPREPLY[@]} -eq 1 ]]; then
        compopt -o nospace
    fi
}

_cd_completion() {
    local cur="${COMP_WORDS[COMP_CWORD]}"
    local envar_name=$(extract_env_var "$cur")
    local cmd="${COMP_WORDS[0]}"
    if [[ "$envar_name" == "" && "$cur" != '$' ]]; then   # completion without environment variable
        readarray -t COMPREPLY < <(compgen -d -- "$cur")
    else
        if [[ "$envar_name" == "$cur" || "$cur" == '$' ]]; then   # not yet completed environment var
            # Get environment variables starting with the prefix
            local prefix=${cur:1}
            get_folder_envars "$prefix"
        else                        # environment var is already completed
            local rest=$(extract_rest "$cur")
            local expanded=$(expand_env_var "$envar_name")
            local complete="$expanded/$rest"
            readarray -t COMPREPLY < <(compgen -d -- "$cur")
        fi
    fi

    # append / to the results that correspond to a folder
    local results=()
    for var in "${COMPREPLY[@]}"; do
        local envar_name=$(extract_env_var "$var")
        local to_check="$var"
        if [[ "$envar_name" != "" ]]; then
            expanded=$(expand_env_var "$envar_name")
            rest=$(extract_rest "$var/")
            to_check="$expanded/$rest"
        fi
        results+=("$var/")
    done
    COMPREPLY=("${results[@]}")

    # Add nospace option if there is only one completion option
    if [[ ${#COMPREPLY[@]} -eq 1 ]]; then
        compopt -o nospace
    fi
}
complete -F '_cd_completion' cd
complete -F '_file_completion' cp
complete -F '_file_completion' mv
complete -F '_file_completion' tvim
