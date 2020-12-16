[![Gitpod ready-to-code](https://img.shields.io/badge/Gitpod-ready--to--code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/luzi82/codelog.flask)

## Example

https://compute-codelog-webtemplate1601-sample.aws-public.luzi82.com

https://static-codelog-webtemplate1601-sample.aws-public.luzi82.com

## Run local

```
aws configure # configure credentials
./local-test.sh
```

## Run in AWS

1. Create domain in AWS Route 53.
1. Create cert for domain.
1. Create and edit `conf/conf.json` from `conf/conf.json.sample`.
1. `./aws-deploy.sh`
