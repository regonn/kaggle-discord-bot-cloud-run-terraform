# Kaggle discord bot for gcp cloud run with terraform

## Push to Container Registry

```
$ cd docker/kaggle_discord_bot_for_cloud_run
$ cp .env.sample .env
```

Fill `.env` file.

```
$ docker build -t kaggle-discord-bot-for-cloud-run .
$ gcloud auth configure-docker
$ docker tag kaggle-discord-bot-for-cloud-run gcr.io/[PROJECT-ID]/kaggle-discord-bot-for-cloud-run
$ docker push gcr.io/[PROJECT-ID]/kaggle-discord-bot-for-cloud-run
```

## Terraform

```
$ cd [This project directory]/terraform
```

Put `account.json` file from [GCP service account keys](https://cloud.google.com/iam/docs/creating-managing-service-account-keys#iam-service-account-keys-create-console)

```
$ terraform init
$ terraform plan
$ terraform apply
```
