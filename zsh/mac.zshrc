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

# Uncomment to change how many often would you like to wait before auto-updates occur? (in days)
# export UPDATE_ZSH_DAYS=13
# Uncomment following line if you want to disable colors in ls
# DISABLE_LS_COLORS="true"
# Uncomment following line if you want to disable autosetting terminal title.
# DISABLE_AUTO_TITLE="true"

DISABLE_CORRECTION="true"
unsetopt correct_all
# Uncomment following line if you want red dots to be displayed while waiting for completion
# COMPLETION_WAITING_DOTS="true"

# Which plugins would you like to load? (plugins can be found in ~/.oh-my-zsh/plugins/*)
# Custom plugins may be added to ~/.oh-my-zsh/custom/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
plugins=(tmux)

source $ZSH/oh-my-zsh.sh
export LANG=zh_CN.UTF-8
# Customize to your needs...

#alias ls="ls -G"
#alias ll="ls -alG"

#test -r /sw/bin/init.sh && . /sw/bin/init.sh
#if [ "$TERM" != "dumb" ]; then
#    export LS_OPTIONS='--color=auto'
#    test -r ~/.dir_color && eval "$(dircolors -b ~/.dir_color)" || eval "$(dircolors -b)"
#    eval `dircolors ~/.dir_color`
#fi
# Useful aliases
#alias ls='ls $LS_OPTIONS'
#alias ll='ls -al'
#alias hdd='/Volumes/HDD'
#alias grep='grep $LS_OPTIONS'
#
bindkey -v
bindkey '\e[3~' delete-char
bindkey '^R' history-incremental-search-backward
bindkey '^P' up-history
bindkey '^N' down-history
bindkey '^H' backward-delete-char
bindkey '^?' backward-delete-char

fancy-ctrl-z () {
if [[ $#BUFFER -eq 0 ]]; then
    bg
    zle redisplay
  else
    zle push-input
  fi
}
zle -N fancy-ctrl-z
bindkey '^Z' fancy-ctrl-z
bindkey '^U' backward-kill-line


#source z.sh
source ~/Develop/dofiles/z/z.sh

#source zsh-syntax-hightlighting
source ~/Develop/dofiles/zsh/zsh-syntax-hightlighting/zsh-syntax-highlighting.plugin.zsh
GHLIGHT_HIGHLIGHTERS=(main brackets pattern cursor)

alias vimpath='cd ~/Documents/foursk/vimfiles'


alias mv 'mv -i'
alias cp 'cp -i'
alias rm 'rm -i'

#Mongo
alias mongo-start='sudo /etc/rc.d/mongo/mongo-start.sh'
alias mongo='/usr/local/mongo/bin/mongo'

#vhost
alias ubuntu='ssh foursk@10.211.55.9'



alias nginx='sudo /usr/local/sbin/nginx'
alias nginx-restart='sudo /usr/local/sbin/nginx -s reload'
