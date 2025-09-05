#! /bin/bash
# set -e
############ HOW TO RUN ####################
# run this script WITHOUT sudo and give    #
# your git acc and login data, otherwise   #
# the repository can't be setup for you!   #
############################################

############### SCRIPT PARAMETERS

current_root=$(pwd)
VENV_NAME=scheduling10_venv

FOLDER_EXISTS=$(test -d "$VENV_NAME" && echo true || echo false)

if ! $FOLDER_EXISTS ; then
    echo '>>>>>>>>>>>>>> NO FOLDER'
    
    echo 'Someone forgot to init this Laptop.
    If you happen to have internet run the init.sh file,
    If you dont have Internet, copy the UARM_env from another laptop into this directory.
    If you have neither...go buy some donuts, you will need them! '
    exit 1
fi

############### START JUPYTER PROJECT/SERVER

source $VENV_NAME/bin/activate

python src/analysis/gui.py
