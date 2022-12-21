"""Simple Flask server for redirecting messages from GoAlert."""
import requests
import re
from mattermostdriver import Driver
from flask import Flask, request
from config import Config

app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health():
    """
    Health check endpoint.
    """

    return "Healthy"


if Config.MATTERMOST_ENABLED:
    mm = Driver(
        {
            "url": Config.MATTERMOST_URL,
            "login_id": Config.MATTERMOST_USER,
            "token": Config.MATTERMOST_PASSWORD,
            "scheme": Config.MATTERMOST_SCHEMA,
            "port": Config.MATTERMOST_PORT,
            "debug": Config.MATTERMOST_DEBUG,
        }
    )
    mm.login()

    @app.route("/mattermost/<username>", methods=["POST"])
    def mm_pm(username):
        """
        Mattermost endpoint for webhooks resend.
        """
        # get info of user to direct message
        to_user = mm.users.get_user_by_username(username)
        # get info of user from direct message(bot called goalert)
        from_user = mm.users.get_user(user_id="me")
        # create list with id from and to users
        peers = [from_user["id"], to_user["id"]]
        # data of post payload
        data = request.json
        # create direct message channel
        direct_channel = mm.channels.create_direct_message_channel(peers)
        # Get GoAlert type from post payload
        if data["Type"] == "Verification":
            mm_data = "GoAlert Verification code is {0}".format(data["Code"])
        elif data["Type"] == "Alert":
            details = re.sub("## Payload.*", "", str(data["Details"]), flags=re.DOTALL)
            mm_data = "[GoAlert-{1}]({0}/alerts/{1}) {2} {3}".format(
                Config.GOALERT_URL, str(data["AlertID"]), data["Summary"], details
            )
        elif data["Type"] == "AlertStatus":
            mm_data = "[GoAlert-{1}]({0}/alerts/{1}) update status {2}".format(
                Config.GOALERT_URL, str(data["AlertID"]), data["LogEntry"]
            )
        elif data["Type"] == "Test":
            mm_data = "This is a [GoAlert]({0}) test message".format(Config.GOALERT_URL)
        # create private message with mm_data text message
        private_message = mm.posts.create_post(
            options={"channel_id": direct_channel["id"], "message": mm_data}
        )

        return private_message
else:
    @app.route("/mattermost/<username>", methods=["POST"])
    def mm_pm(username):
        """
        Mattermost endpoint for webhooks resend.
        """
        return "Mattermost endpoint not Enabled"

if Config.TELEGRAM_ENABLED:
    @app.route("/telegram/<username>", methods=["POST"])
    def tg_pm(username):
        """
        Telegram endpoint for webhooks resend.
        """
        token = Config.TELEGRAM_TOKEN
        url = f"https://api.telegram.org/bot{token}/sendMessage?parse_mode=Markdown"

        # data of post payload
        data = request.json
        # Get GoAlert type from post payload
        if data["Type"] == "Verification":
            tg_data = "GoAlert Verification code is {0}".format(data["Code"])
        elif data["Type"] == "Alert":
            details = re.sub("## Payload.*", "", str(data["Details"]), flags=re.DOTALL)
            tg_data = "[GoAlert-{1}]({0}/alerts/{1}) {2} {3}".format(
                Config.GOALERT_URL, str(data["AlertID"]), data["Summary"], details
            )
        elif data["Type"] == "AlertStatus":
            tg_data = "[GoAlert-{1}]({0}/alerts/{1}) update status {2}".format(
                Config.GOALERT_URL, str(data["AlertID"]), data["LogEntry"]
            )
        elif data["Type"] == "Test":
            tg_data = "This is a [GoAlert]({0}) test message".format(Config.GOALERT_URL)

        data = {"chat_id": username, "text": tg_data}
        private_message = requests.post(url, data).json()

        return private_message
else:
    @app.route("/telegram/<username>", methods=["POST"])
    def tg_pm(username):
        """
        Telegram endpoint for webhooks resend.
        """
        return "Telegram endpoint not Enabled"

if __name__ == "__main__":
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
