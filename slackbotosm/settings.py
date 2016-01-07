import os

DEBUG = False

GEOWATCH_BROKER_OSM = {
    "enabled": True,
    "name": "Slack Bot for OpenStreetMap",
    "description": "This broker responds to /osm in Slack Channels",
    "consumers":
    [
        {
            "backend": "slack",
            "codec": "json",
            "topic": "test",
            "topic_check": False # Slack API doesn't support bot's joining channels automatically.  Need to do /invite @botname in channel UI.
        }
    ]
}

try:
    from local_settings import *  # noqa
except ImportError:
    pass
