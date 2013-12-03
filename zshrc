# Path to your oh-my-zsh configuration.
ZSH=$HOME/.oh-my-zsh

# Set name of the theme to load.
# Look in ~/.oh-my-zsh/themes/
# Optionally, if you set this to "random", it'll load a random theme each
# time that oh-my-zsh is loaded.
ZSH_THEME="wedisagree"

# Example aliases
# alias zshconfig="mate ~/.zshrc"
# alias ohmyzsh="mate ~/.oh-my-zsh"

# Set to this to use case-sensitive completion
# CASE_SENSITIVE="true"

# Comment this out to disable bi-weekly auto-update checks
# DISABLE_AUTO_UPDATE="true"

# Uncomment to change how often before auto-updates occur? (in days)
# export UPDATE_ZSH_DAYS=13

# Uncomment following line if you want to disable colors in ls
# DISABLE_LS_COLORS="true"

# Uncomment following line if you want to disable autosetting terminal title.
# DISABLE_AUTO_TITLE="true"

# Uncomment following line if you want to disable command autocorrection
DISABLE_CORRECTION="true"

# Uncomment following line if you want red dots to be displayed while waiting for completion
# COMPLETION_WAITING_DOTS="true"

# Uncomment following line if you want to disable marking untracked files under
# VCS as dirty. This makes repository status check for large repositories much,
# much faster.
# DISABLE_UNTRACKED_FILES_DIRTY="true"

# Which plugins would you like to load? (plugins can be found in ~/.oh-my-zsh/plugins/*)
# Custom plugins may be added to ~/.oh-my-zsh/custom/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
plugins=(git svn)

export PIP2EVAL_TMP_FILE_PATH=/tmp/shm


source $ZSH/oh-my-zsh.sh
source /home/foursk/Develop/dofiles/z.sh


bindkey -v
bindkey '\e[3~' delete-char
bindkey '^F' history-incremental-search-backward

# Customize to your needs...
# set -o vi
set -o vi
alias ll='ls -alh'
alias gdd="git add .&&git commit -m 'update'"

#ssh
alias ssh-aliyun="ssh root@112.124.55.59"


#mongo
alias mongo-start="sudo /usr/local/mongo/servers/mongo-start.sh"
alias mongo-openvim="sudo /usr/local/mongo/bin/mongo 127.0.0.1:27017/openvim -uopenvim -p"

alias apa-restart="sudo apachectl restart"


#vim
alias govim="cd ~/.vim"

#alias cd
alias ..="cd .."
alias ..2="cd ../.."
alias ..3="cd ../../.."
alias ..4="cd ../../../.."



#jjshouse
alias gojjs="cd ~/workspace/jjshouse/"
alias gov5="cd ~/workspace/jjshouse/v5/"
alias gounit="cd ~/workspace/jjshouse/v5/vendor/blu3gui7ar/esmeralda/test/"

alias phpunit="/home/foursk/workspace/jjshouse/v5/vendor/blu3gui7ar/esmeralda/vendor/phpunit/phpunit/phpunit.php"
alias phpunit-coverage="/home/foursk/workspace/jjshouse/v5/vendor/blu3gui7ar/esmeralda/vendor/phpunit/phpunit/phpunit.php --coverage-html"

unsetopt correct_all





setopt extended_glob

TOKENS_FOLLOWED_BY_COMMANDS=('|' '||' ';' '&' '&&' 'sudo' 'do' 'time' 'strace')

recolor-cmd() {
region_highlight=()
colorize=true
start_pos=0
for arg in ${(z)BUFFER}; do
((start_pos+=${#BUFFER[$start_pos+1,-1]}-${#${BUFFER[$start_pos+1,-1]## #}}))
((end_pos=$start_pos+${#arg}))
if $colorize; then
colorize=false
res=$(LC_ALL=C builtin type $arg 2>/dev/null)
case $res in
'reserved word') style="fg=magenta,bold";;
'alias for') style="fg=cyan,bold";;
'shell builtin') style="fg=yellow,bold";;
'shell function') style='fg=green,bold';;
"$arg is")
[[ $arg = 'sudo' ]] && style="fg=red,bold" || style="fg=blue,bold";;
*) style='none,bold';;
esac
region_highlight+=("$start_pos $end_pos $style")
fi
[[ ${${TOKENS_FOLLOWED_BY_COMMANDS[(r)${arg//|/|}]}:+yes} = 'yes' ]] && colorize=true
start_pos=$end_pos
done
}
check-cmd-self-insert() { zle .self-insert && recolor-cmd }
check-cmd-backward-delete-char() { zle .backward-delete-char && recolor-cmd }

zle -N self-insert check-cmd-self-insert
zle -N backward-delete-char check-cmd-backward-delete-char
