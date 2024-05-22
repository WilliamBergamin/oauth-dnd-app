import json
import logging
import os
import time
from typing import TypedDict

from slack_bolt import App, BoltContext, Complete, Fail
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient
from slack_bolt.oauth.oauth_settings import OAuthSettings
from slack_sdk.oauth.installation_store import FileInstallationStore

SLACK_BASE_URL = os.getenv("SLACK_BASE_URL", "https://slack.com")

app = App(
    client=WebClient(base_url=f"{SLACK_BASE_URL}/api/"),
    attaching_function_token_enabled=False,
    installation_store=FileInstallationStore(base_dir="./data/installations"),
    signing_secret=os.environ["SLACK_SIGNING_SECRET"],
    oauth_settings=OAuthSettings(
        authorization_url=f"{SLACK_BASE_URL}/oauth/v2/authorize",
        client_id=os.environ["SLACK_CLIENT_ID"],
        client_secret=os.environ["SLACK_CLIENT_SECRET"],
        user_scopes=["dnd:write", "dnd:read"],
    ),
)
logging.basicConfig(level=logging.INFO)


class UserContext(TypedDict):
    id: str
    secret: int


def build_user_client(user_context: UserContext, context: BoltContext) -> WebClient:
    installation = app.installation_store.find_installation(
        enterprise_id=context.enterprise_id, team_id=context.team_id, user_id=user_context["id"]
    )
    return WebClient(token=installation.user_token, base_url=f"{SLACK_BASE_URL}/api/")


@app.function("set_snooze")
def handle_set_snooze_event(context: BoltContext, inputs: dict, complete: Complete, fail: Fail, logger: logging.Logger):
    user_client = build_user_client(inputs["user"], context)
    try:
        response = user_client.dnd_setSnooze(num_minutes=inputs["snooze_until"] - int(time.time()))
        logger.info(json.dumps(response.data, indent=2))
        complete({"snooze_endtime": response.data["snooze_endtime"]})
    except Exception as e:
        logger.exception(e)
        fail(f"Failed to handle a function request (error: {e})")


@app.function("end_snooze")
def handle_end_snooze_event(context: BoltContext, inputs: dict, complete: Complete, fail: Fail, logger: logging.Logger):
    user_client = build_user_client(inputs["user"], context)
    try:
        response = user_client.dnd_endSnooze()
        logger.info(json.dumps(response.data, indent=2))
        complete({"snooze_endtime": response.data["next_dnd_end_ts"]})
    except Exception as e:
        logger.exception(e)
        fail(f"Failed to handle a function request (error: {e})")


if __name__ == "__main__":
    SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).connect()
    app.start()
