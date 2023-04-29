# more natural completion of cd with environment variables
# Usage:
#   Source this file, for example in your ~/.bashrc or similar. e.g.
#   source cd_completion.sh
# XXX Improvements:
# - when starting with $envvar, it should keep it
# - when already ending by /, it shouldn't append another /
# - when there's just one $envvar, it should select it by appending /
#
_cd_completion() {
    local cur="${COMP_WORDS[COMP_CWORD]}"
    local prefix

    # Return the starting environment variable from the string in $1
    extract_env_var() {
        if [[ "$1" == *"$"* ]]; then
            echo "$1" | grep -o '$[a-zA-Z_][a-zA-Z_0-9]*'
        else
            echo ""
        fi
    }

    # Returns the corresponding value of a environment variable whose name is in $1
    expand_env_var() {
        # Get the value of the environment variable and append a slash
        prefix="${1%/}"
        prefix=${prefix:1}
        echo "${!prefix}"
    }

    # Returns the contents after an starting environment variable
    extract_rest() {
        echo "${1#*/}"
    }

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

    envar_name=$(extract_env_var "$cur")
    ### echo
    ### echo "XXX cur: |$cur| envar_name: |$envar_name|"
    if [[ "$envar_name" == "" && "$cur" != '$' ]]; then   # completion without environment variable
        # Get directories
        readarray -t COMPREPLY < <(compgen -d -- "$cur")
        for i in "${!COMPREPLY[@]}"; do
            COMPREPLY[$i]="${COMPREPLY[$i]%/}"
        done
    else
        if [[ "$envar_name" == "$cur" || "$cur" == '$' ]]; then   # not yet completed environment var
            ### echo
            ### echo "XXX envar_name==cur: $envar_name"
            # Get environment variables starting with the prefix
            prefix=${cur:1}
            get_env_vars "$prefix"
        else                        # environment var is already completed
            rest=$(extract_rest "$cur")
            expanded=$(expand_env_var "$envar_name")
            complete="$expanded/$rest"
            ### echo
            ### echo "XXX envar_name: |$envar_name| rest: |$rest| expanded: |$expanded| complete: |$complete|"
            readarray -t COMPREPLY < <(compgen -d -- "$cur")
            ### for i in "${!COMPREPLY[@]}"; do
            ###     echo "XXX When i: |$i| COMPREPLY[i]: |${COMPREPLY[$i]}|"
            ###     relative=$(get_relative_path "${COMPREPLY[$i]}" "$expanded")
            ###     COMPREPLY[$i]="$envar_name/$relative"
            ###     echo "XXX relative: |$relative| COMPREPLY[i]: |${COMPREPLY[$i]}|"
            ### done
        fi
    fi


    ## if [[ "$cur" == \$* && "$cur" != *\/ ]]; then
    ##     # Get environment variables starting with the prefix
    ##     prefix=${cur:1}
    ##     get_env_vars "$prefix"
    ## elif [[ "$cur" == \$*\/ ]]; then
    ##     # Get the value of the environment variable and append a slash
    ##     prefix="${cur%/}"
    ##     prefix=${prefix:1}
    ##     COMPREPLY="${!prefix}"/
    ## else
    ##     # Get directories
    ##     readarray -t COMPREPLY < <(compgen -d -- "$cur")
    ##     for i in "${!COMPREPLY[@]}"; do
    ##         COMPREPLY[$i]="${COMPREPLY[$i]%/}/"
    ##     done
    ## fi

    # Add nospace option if there is only one completion option
    if [[ ${#COMPREPLY[@]} -eq 1 ]]; then
        compopt -o nospace
    fi
}
complete -F '_cd_completion' cd
