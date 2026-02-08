# Monobank Send Comment Bot

This is a Telegram bot that allows users to specify comments in send.monobank.ua links.
You can run it on AWS Lambda, on a server, or even on your local machine.

## Using this bot

To use the bot, copy source code to your machine.
Build the Docker image using the provided Dockerfile and specify the necessary environment variables (see [Configuration](#configuration) section below).
Then run the container.
Depending on the configuration, the bot will start polling for updates or set up a webhook.

### Lambda deployment

To use the bot on AWS Lambda, build the `lambda.Dockerfile` image and push it to ECR.
Then create a new Lambda function using the image and specify the necessary environment variables (see [Configuration](#configuration) section below).
Bot will not set up the webhook, so you'll have to make a separate request to Telegram's bot API, like so:

```bash
curl https://api.telegram.org/bot<your_bot_token>/setWebhook?url=<function_url>
```

This step may be automated with a use of build/push/deploy scripts, but isn't here.

## Configuration

See example.env for the general configuration.

You can configure the bot for one of three modes:
1. Pooling mode;
2. Webhook mode;
3. Lambda mode (webhook but without the need to set up a server).

In general, all modes require you to set the `BOT_TOKEN` environment variable to your bot's token, which you can get from the BotFather on Telegram.

### Pooling mode

For pooling mode, set the `USE_POOLING` environment variable to `true` and the bot will start polling for updates when you run it.

### Webhook mode

In webhook mode, you need to set `WEBHOOK_BASE_URL` to the base URL of your webhook endpoint, e.g. `https://yourdomain.com` or `https://yourdomain.com/webhook`. The bot will set up the webhook when you run it.

Unless, of course, you don't want it to. Then specify `SET_WEBHOOK_ON_STARTUP` variable and set it to `false`.

### Lambda mode

In Lambda mode you should use the lambda.Dockerfile to build a Docker image and deploy it to AWS Lambda. The bot will be triggered by incoming webhook requests. (You can experiment with this by running [lambda.py](/src/lambda.py) locally and providing the necessary arguments)

Then - specify `BOT_TOKEN`, `SECRET`, and `WEBHOOK_BASE_URL` environment variables in your Lambda function configuration. The bot will set up the webhook when it receives the first request.
While `SECRET` and `WEBHOOK_BASE_URL` are not necessary for the operation, you still have to specify them, for now.
