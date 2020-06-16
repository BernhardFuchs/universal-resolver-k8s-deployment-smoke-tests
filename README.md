# universal-resolver-k8s-deployment-smoke-tests

## Build container with

    docker build -f Dockerfile -t smoke-test .
    
## Run container with

    docker run -it --rm -e INGRESS_FILE=<path-to-uniresolver-ingress.yaml> -e CONFIG_FILE=<path-to-config.json> --name smoke-test smoke-test
