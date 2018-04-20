#!/bin/bash
# The requirements.sh is an advanced mechanism an should rarely be needed.
# Be aware that it won't run with root permissions and 'sudo' won't work
# in most cases.

#detect distribution using lsb_release (may be replaced parsing /etc/*release)
dist=$(lsb_release -ds)
dependencies=( nmap )

#setting dependencies and package manager in relation to the distribution
if $(hash pkcon 2>/dev/null); then
    pm="pkcon install -y"
    dependencies=( nmap liblinear1 )
else
    priv="sudo"
    if [ "$dist"  == "\"Arch Linux\""  ]; then
        pm="pacman -S"
    elif [[ "$dist" =~  "Ubuntu" ]] || [[ "$dist" =~ "Debian" ]] ||[[ "$dist" =~ "Raspbian" ]]; then
        pm="apt install"
    elif [[ "$dist" =~ "SUSE" ]]; then 
        pm="zypper install"
    fi
fi

# installing dependencies
if [ ! -z "$pm" ]; then
    for dep in "${dependencies[@]}"
    do
        $priv $pm $dep
    done
fi
