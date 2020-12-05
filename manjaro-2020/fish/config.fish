### Environment variables ##

set EDITOR /usr/bin/nvim
set TERMINAL /usr/bin/kitty
set VISUAL /usr/bin/nvim
set BROWSER /usr/bin/firefox
set SHELL /usr/bin/fish
set PATH ~/.nvm/versions/node/v14.15.0/bin $PATH
# or: export PATH=/home/daniel/.nvm/versions/node/v14.15.0/bin:$PATH

# - end Environment variables #


### Functions ###

function d-backup-config --argument-names commit_message --description "Backup my config files"
	set --local DOTFILES "$HOME/Projects/dotfiles"
	git -C "$DOTFILES" add -A
	if test (count $argv) = 1 && "$commit_message" != ""
		git -C $DOTFILES commit -m "$commit_message"
	else
		git -C $DOTFILES commit -m "updated"
	end
	git -C $DOTFILES push origin
	git -C $DOTFILES push github
end

function d-fast-backup-config -d "Backup my config files without output"
	set --local DOTFILES "$HOME/Projects/dotfiles"
	git -C "$DOTFILES" add -A > /dev/null
	git -C $DOTFILES commit -m "updated" > /dev/null
	git -C $DOTFILES push origin > /dev/null
	git -C $DOTFILES push github > /dev/null
end

function d-cd
	cd $argv[1]
	d-list
end

function d-backup
	d-copy $1{,~}
	echo "Created backup $1.~"
end

function d-sbackup
	d-scopy $1{,.bak}
	echo "Created backup as 'root': $1.bak"
end

function d-copyclip
	xclip -sel c < $1 
end

function d-scopyclip
	doas xclip -sel c < $1
end

function d-python --argument-names file_name --description "Compile, type check and run python file"
	python3 -m py_compile $file_name
	if test $status != 0
		return 1
	end
	mypy $file_name
	if test $status != 0
		return 2
	end
	python3 $file_name
end

function d-clang --argument-names file_name
	d-clangc $file_name -o $file_name".out"
	if test $status != 0
		return 1
	end
	./$file_name".out"
end

# - end Functions #


### Aliases ##

alias br="broot"
alias d-windowName="xprop | grep WM_NAME"
alias d-windowClass="xprop | grep WM_CLASS"
alias d-man="tldr"
alias d-findPackage="apt list -a"
alias d-clangc="clang++ -Wall -std=c++17"
alias d-pm-install="doas pacman -Syu"
alias d-pm-search="pacman -Ss"
alias d-pm-update="doas pacman -Sy"
alias d-pm-clean="doas pacman -Rns (pacman -Qdtq)"
alias d-yay-install="yay -Syu"
alias d-yay-search="yay -Ss"
alias d-yay-clean="yay -Yc"
alias d-pm-upgrade="doas pacman -Syu"
alias d-yay-upgrade="yay -Syu"
alias d-yay-remove="yay -Rns"
alias d-pm-remove="doas pacman -Rsc"
alias d-list='lsd -laA --classify --date "+%b %e %T"'
alias d-list-trash="gio list -lh trash://"
alias d-open="gio open"
alias d-show="bat"
alias d-edit="nvim"
alias d-editcsv="sc-im"
alias d-seditcsv="sc-im"
alias d-sedit="doas nvim"
alias d-editT="nvim -p"
alias d-seditT="doas nvim -p"
alias d-editV="nvim -O"
alias d-seditV="doas nvim -O"
alias d-editH="nvim -o"
alias d-seditH="doas nvim -o"
alias d-sshow="doas bat"
alias d-copy="gio copy --progress --interactive"
alias d-copyb="d-copy --backup"
alias d-move="gio move --progress --interactive"
alias d-moveb="d-move --backup"
alias d-scopy="doas gio copy --progress --interactive"
alias d-scopyr="doas cp --recursive --interactive"
alias d-scopyb="doas d-copy --backup"
alias d-smove="doas gio move --progress --interactive"
alias d-smoveb="doas d-move --backup"
alias d-rename="gio rename"
alias d-srename="doas gio rename"
# alias d-tree="gio tree"
alias d-tree='lsd -laA --classify --tree --depth 3 --date "+%b %e %H:%M" --blocks name'
alias d-trash="gio trash"
alias d-strash="doas gio trash"
alias d-mkdir="gio mkdir --parent"
alias d-smkdir="doas gio mkdir --parent"
alias d-man="tldr"
alias d-search="br -h" # broot
alias d-hardlink="ln"
alias d-shardlink="doas ln"
alias d-symlink="ln -s"
alias d-ssymlink="doas ln -s"
alias d-zsh="d-edit ~/.zshrc"
alias d-fish="d-edit ~/.config/fish/config.fish"
alias d-vim="d-edit ~/.config/nvim/init.vim"
alias d-qtile="d-edit ~/.config/qtile/config.py"

# - end Aliases #


### Abbreviations ###

abbr git-acp 'git add . && git commit -m "updated" && git push'
abbr cd 'd-cd'
abbr ll 'd-list'

# - end Abbreviations #


### Autostart commands ###
fish_vi_key_bindings # vi mode
# paleofetch			 # display pc info

# - end Autostart commands # 
