#! /bin/bash
echo "Updater of rust alternatives"
echo "- rustup update"
echo "- delta   -> diff"
echo "- bat     -> cat"
echo "- exa     -> ls"
echo "- dust    -> du"
echo "- ripgrep -> grep"
echo "- fd      -> find"
echo "- alacritty"
echo "- starship"
echo "- tokey"
echo "ATTENTION: it will take some time. You can abort it by ctrl-c"
read -r VAR
nice rustup update
delta --version
exa --version
dust --version
starship --version
rg --version
tokei --version
alacritty --version
nice cargo install ripgrep --features pcre2
nice cargo install git-delta
nice cargo install --locked bat
nice cargo install --locked exa
nice cargo install du-dust
nice cargo install --locked starship
nice cargo install --locked ripgrep
nice cargo install --locked tokei
nice cargo install --locked fd-find
nice cargo install alacritty
echo done
