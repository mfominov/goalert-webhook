# How to

1. Build docker image

  ```bash
  docker build -t golaert-webhook:latest .
  ```

1. Run docker image

  ```bash
  docker run --rm -it -p 8080:8080 golaert-webhook:latest
  ```

1. Run pre-build image

  ```bash
  docker run --rm -it -p 8080:8080 mfominov/goalert-webhook:latest
  ```

2. Environment variables

| Variable            | Description                                            |
| ------------------- | ------------------------------------------------------ |
| MATTERMOST_ENABLED  | Enable/Disable Mattermost context path(default: False) |
| MATTERMOST_URL      | Mattermost server url(default: chat.example.com)       |
| MATTERMOST_PORT     | Mattermost port(default: 443)                          |
| MATTERMOST_SCHEMA   | Mattermost schema(default: http)                       |
| MATTERMOST_USER     | Mattermost user(create bot account)                    |
| MATTERMOST_PASSWORD | Mattermost password(create bot account)                |
| MATTERMOST_DEBUG    | Mattermost plugin debug output(default: False)         |
| TELEGRAM_ENABLED    | Enable/Disable Telegram context path(default: False)   |
| TELEGRAM_TOKEN      | Telegram bot token                                     |
| GOALERT_URL         | GoAlert server url(default: https://chat.example.com)  |
| DEBUG               | Enable/Disable Flask debug(default: false)             |
| PORT                | Flask app port(default: 8080)                          |
| HOST                | Flask app host(default: 0.0.0.0)                       |
