[![Gitpod ready-to-code](https://img.shields.io/badge/Gitpod-ready--to--code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/luzi82/codelog.flask)

# codelog.flask

This project show how flask works.
If you want to create new project, use https://github.com/luzi82/codelog.web-template.1601 .

## Example

https://compute-codelog-webtemplate1601-sample.aws-public.luzi82.com

https://static-codelog-webtemplate1601-sample.aws-public.luzi82.com

## Run gitpod

```
./s01_local_run.sh
```

## Run local

```
aws configure # configure credentials
./s00_init_workspace.sh
./s01_local_run.sh
```

## Deploy to AWS

1. Create domain in AWS Route 53.
1. Create cert for domain.
1. Create and edit `conf/conf.json` from `conf/conf.json.sample`.
1. `./s50_aws_init_env.sh && ./s51_aws_deploy.sh`

## Undeploy from AWS

1. `./s50_aws_init_env.sh && ./s59_aws_undeploy.sh`
