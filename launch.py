from geowatchutil.runtime import build_broker_kwargs

from slackbotosm import settings
from slackbotosm import templates
from slackbotosm.broker.base import SlackBotOSMBroker

verbose = True
broker_config = settings.GEOWATCH_BROKER_OSM
broker_kwargs = build_broker_kwargs(
    broker_config,
    settings.GEOWATCH_CONFIG,
    templates=templates,
    verbose=verbose)

print "KWARGS: ", broker_kwargs

broker = SlackBotOSMBroker(
    broker_config.get('name', None),
    broker_config.get('description', None),
    **broker_kwargs)
broker.run()
