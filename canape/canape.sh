#!/bin/bash

site_home=$(dirname $0)
web_pid=0


function clean()
{

  echo "Cleaning"

  rm -fvr $site_home/deploy

}

function local()
{
  echo "Running server"  
  hyde -s $site_home -w -k &
  web_pid=$!

  echo "Running generator"
  hyde -s $site_home -g -k

}

function server()
{
  echo "Running server"  
  hyde -s $site_home -w -k
}

function generate()
{

  clean
  hyde -s $site_home -g

}

function publish
{
  echo "Publishing"

  generate

  read -s -p "FTP password: " password
  pushd .
  cd $site_home/deploy
  wput -u * "ftp://canape@fikovnik.net:$password@fikovnik.net/"
  popd
}

function control_c() 
{
  echo -en "\n*** Exiting ***\n"
  if [ $web_pid != 0 ]; then
    kill -9 $web_pid  
  fi
  exit 1
}


# trap keyboard interrupt (control-c)
trap control_c SIGINT

case "$1" in
clean)	
    clean
	  ;;
server)
    server  
    ;;
local)
    local  
    ;;
generate)
    generate
    ;;
publish)
    publish
    ;;
*)	
    echo "Usage: $0 {clean|server|local|publish|generate}"
    exit 2
    ;;
esac

