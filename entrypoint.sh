#!/bin/sh

echo "#### Smoketest for the Universal Resolver Kubernetes Deployment ####"

echo "$HOST"
echo "$CONFIG"

echo "Current folder"
pwd
ls -al

echo "Deployment folder"
ls -al deploy

echo "Root folder"
ls -al /

echo "#### Ingress file ####"
cat /github/workspace/deploy/uni-resolver-ingress.yaml

python --version

# shellcheck disable=SC2164
python /smoke-tests/smoke-test.py --host "$HOST" --config "$CONFIG"
