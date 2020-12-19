[![Gitpod ready-to-code](https://img.shields.io/badge/Gitpod-ready--to--code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/luzi82/codelog.flask)

## Example

https://codelog-flask-sample.aws-public.luzi82.com

## Run gitpod

```
./s01_local_run.sh
```

## Run local

```
./s00_init_workspace.sh
./s01_local_run.sh
```

## Run in AWS

1. Create domain in AWS Route 53.
1. Create cert for domain.
1. Create and edit `conf/conf.json` from `conf/conf.json.sample`.
1. `./aws-deploy.sh`
