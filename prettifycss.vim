" A simple function to prettify CSS code
" Usage:
" 1. load css file
" 2. load this function wit :so prettifycss.vim
" 3. call the function with :call PrettifyCSS()
function! PrettifyCSS()
    %s_\*/_&\r_g
    s/[,:]/& /g
    %s/[{;]/&\r/g
    %s/}/;\r}\r\r/g
    normal gg=G
endfunction
