## Build & Push Docker

```sh
$ VERSION=<tag> DOCKER_REGISTRY=<registry> make docker-push
```

* Update `deploy.yaml` with the pushed image name.

## Deploy

### Generate certificates

First generate a self-signed key and certificate that the server & client can use for TLS.

```sh
$ make keys
```

### Deploy https server & client application running in a kubernetes cluster

Create the TLS secrets.

```sh
$ kubectl create secret tls python-https-test-client-certs --key /tmp/client.key --cert /tmp/client.crt
$ kubectl create secret tls python-https-test-server-certs --key /tmp/server.key --cert /tmp/server.crt
```

Deploy client & server.

```sh
$ kubectl apply -f deploy.yaml
```

## Note
Based on https://github.com/pixie-io/pixie-demos/tree/main/openssl-tracer/ssl_client_server
