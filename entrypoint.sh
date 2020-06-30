#!/bin/sh

echo "#### Smoketest for the Universal Resolver Kubernetes Deployment ####"

sh -c "echo $*"

echo "$INPUT_HOST"
echo "$INPUT_CONFIG"
echo "$INPUT_OUT_FOLDER"

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

python /smoke-tests/smoke-test.py --host "$INPUT_HOST" --config "$INPUT_CONFIG" --out "$INPUT_OUT_FOLDER"

ls -al /smoke-tests
