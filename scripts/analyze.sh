#!/bin/bash -ex

readonly SCRIPTS_DIR=$(dirname "$0")
readonly PROJECT_DIR=$(dirname ${SCRIPTS_DIR})
PYLINT_ARGS="--rcfile=${PROJECT_DIR}/configs/pylint/pylint.cfg"
PYCODESTYLE_ARGS="--max-line-length=120"

log () {
  echo '===============>' "$@"
}

usage () {
  echo
  echo "Usage $0: -d <directories containing source code>"
  echo "  -d: Space separated list of directories containing source code to be analyzed"
  echo "  -t: Directory containing source code for tests"
  echo ""

  exit 1
}


SRC_CODE_DIRS=""
TEST_DIR="tests"

while getopts ":d:t:" opts;
do
  case "${opts}" in
    d)
      SRC_CODE_DIRS=${OPTARG}
      ;;
    t)
      TEST_DIR=${OPTARG}
      ;;
    *)
      usage
      ;;
  esac
done


main () {
  if [ -z "${SRC_CODE_DIRS}" ]; then
    usage
  fi

  rc=0
  for src_code_dir in $SRC_CODE_DIRS;
  do

    log "Analyzing source code in: ${src_code_dir}"

    if ! pycodestyle $PYCODESTYLE_ARGS "$src_code_dir" ;
    then
      rc=$((rc + 1))
    fi

    # Disable duplicate code check for directory containing tests
    if [[ "$src_code_dir" == "$TEST_DIR" ]] ;
    then
      PYLINT_ARGS="--disable duplicate-code $PYLINT_ARGS"
    fi

    if ! pylint $PYLINT_ARGS "$src_code_dir" ;
    then
      rc=$((rc + 1))
    fi

  done

  if [[ "$rc" != "0" ]];
  then
    log "Warnings found in code."

    return 1
  fi

}


main "$@"
