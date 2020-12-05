" ######################## Vim-plug plugins ########################
" $HOME/.local/share/nvim/plugged
call plug#begin(stdpath('data') . '/plugged')
" Theming
" Plug 'itchyny/lightline.vim'
Plug 'vim-airline/vim-airline'
" "Plug 'vim-airline/vim-airline-themes'
Plug 'morhetz/gruvbox'
Plug 'joshdick/onedark.vim'
Plug 'KeitaNakamura/neodark.vim' " Good for Ruby
Plug 'larsbs/vimterial_dark'
Plug 'drewtempelmeyer/palenight.vim'
 
" Improve languages syntax highlight
Plug 'pangloss/vim-javascript'
Plug 'mxw/vim-jsx'
Plug 'othree/html5.vim'
Plug 'vim-language-dept/css-syntax.vim'
Plug 'mattn/emmet-vim'
Plug 'dag/vim-fish'

Plug 'turbio/bracey.vim', {'do': 'npm install --prefix server'}
Plug 'MattesGroeger/vim-bookmarks'
Plug 'tpope/vim-fugitive'
Plug 'preservim/nerdtree'
" Plug 'chrisbra/Colorizer'
Plug 'neoclide/coc.nvim', {'branch': 'release'}
" you need to install a lot of coc plugins for this. For python you need pip and jedi (?), coc-pyright for python with mypy works great
call plug#end()

" ######################## Basic config ########################
syntax on

set number relativenumber
set mouse=a
set noexpandtab
set autoindent " copyindent
set preserveindent
set softtabstop=4
set shiftwidth=4
set tabstop=4

function SetTabs()
	set noexpandtab
	set softtabstop=4
	set shiftwidth=4
	set tabstop=4
endfunction

" Invisible characters
set list
" set listchars=tab:→\ ,space:·,nbsp:␣,trail:•,eol:¶,precedes:«,extends:»
set listchars=tab:\|\ ,space:·,nbsp:␣,trail:•,eol:¶,precedes:«,extends:»
highlight SpecialKey ctermfg=8 guifg=DimGrey

" set foldmethod=syntax
" set foldminlines=30
" set foldnestmax=4

" ######################## Files ########################
" au => autocmd
" au FileType javascript set omnifunc=javascriptcomplete#CompleteJS
" au FileType html set omnifunc=htmlcomplete#CompleteTags
" au FileType css set omnifunc=csscomplete#CompleteCSS
" au FileType php set omnifunc=phpcomplete#CompletePHP

autocmd FileType ruby call SetNeoDarkTheme()
autocmd FileType javascript call SetVimterialTheme()
autocmd FileType html call SetVimterialTheme()
autocmd FileType * call SetTabs()

" autocomplete with </   :iabbrev </ </<C-X><C-O>

" ######################## THEMING ########################

" True colors
if (has("nvim"))
  "For Neovim 0.1.3 and 0.1.4 < https://github.com/neovim/neovim/pull/2198 >
  let $NVIM_TUI_ENABLE_TRUE_COLOR=1
endif

"For Neovim > 0.1.5 and Vim > patch 7.4.1799 < https://github.com/vim/vim/commit/61be73bb0f965a895bfb064ea3e55476ac175162 >
"Based on Vim patch 7.4.1770 (`guicolors` option) < https://github.com/vim/vim/commit/8a633e3427b47286869aa4b96f2bfc1fe65b25cd >
" < https://github.com/neovim/neovim/wiki/Following-HEAD#20160511 >
if (has("termguicolors"))
  set termguicolors
endif

" Theme setup
set background=dark
set cursorline

function SetPaleNight()
	colorscheme palenight
	" let g:lightline = { 'colorscheme': 'palenight' }
	let g:palenight_terminal_italics = 1
	AirlineTheme palenight
endfunction

function SetGruvBoxTheme()
	colorscheme gruvbox
	let g:gruvbox_terminal_italics = 1
	let g:airline_powerline_fonts = 1
"	AirlineTheme gruvbox
endfunction

function SetOneDarkTheme()
	colorscheme onedark
	let g:onedark_terminal_italics = 1
	let g:airline_powerline_fonts = 1
	let g:airline_theme = "onedark"
endfunction

function SetNeoDarkTheme()
	let g:neodark#background = '#202020'
	let g:neodark#solid_vertsplit = 1
	let g:airline_powerline_fonts = 1
	let g:neodark_terminal_italics = 1
	colorscheme neodark
	AirlineTheme neodark
endfunction

function SetVimterialTheme()
	let g:airline_theme='vimterial_dark'
	colorscheme vimterial_dark
	AirlineTheme vimterial_dark
endfunction

call SetGruvBoxTheme()

" ######################## Extra config ########################

let g:colorizer_auto_filetype='css,html,vim,lua,conf'
let g:user_emmet_install_global = 0
autocmd FileType html,css,jsx,javascriptreact EmmetInstall

" ######################## Abbreviations and maps ########################

" Vim bookmarks customization:
nmap <Leader><Leader> <Plug>BookmarkToggle
nmap <Leader>i <Plug>BookmarkAnnotate
nmap <Leader>a <Plug>BookmarkShowAll
nmap <Leader>j <Plug>BookmarkNext
nmap <Leader>k <Plug>BookmarkPrev
nmap <Leader>c <Plug>BookmarkClear
nmap <Leader>x <Plug>BookmarkClearAll
nmap <Leader>kk <Plug>BookmarkMoveUp
nmap <Leader>jj <Plug>BookmarkMoveDown
nmap <Leader>g <Plug>BookmarkMoveToLine

" COC maps

" Nerdtree config
map <C-n> :NERDTreeToggle<CR>

