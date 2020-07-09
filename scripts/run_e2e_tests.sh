#!/bin/bash

readonly SCRIPTS_DIR=$(dirname "$0")
readonly PROJECT_DIR=$(dirname "${SCRIPTS_DIR}")
readonly TESTS_DIR="${PROJECT_DIR}/tests"
readonly ENDPOINT_BASE_URL="${ENDPOINT_BASE_URL}"

if [[ -z "$ENDPOINT_BASE_URL" ]]; then
    echo "*** No ENDPOINT_BASE_URL specified, stopping e2e test execution ***"
    exit 1
fi

TEST_TAG_PARAM=""

if [ -n "$TEST_TAG" ]; then
  TEST_TAG_PARAM="-m $TEST_TAG"
fi

echo "Running E2E test with endpoint base url $ENDPOINT_BASE_URL"

pytest $TESTS_DIR/e2e --no-cov -v $TEST_TAG_PARAM
