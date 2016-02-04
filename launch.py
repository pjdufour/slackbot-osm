import yaml

from geowatchutil.runtime import build_broker_kwargs

from slackbotosm import settings
from slackbotosm.broker.base import SlackBotOSMBroker
from slackbotosm.utils import load_templates

verbose = True

broker_config = None
with open("slackbotosm/bot.yml", 'r') as f:
    broker_config = yaml.load(f)
#print "Broker Config: ", broker_config

templates = load_templates()
#print "##############"
#print "Templates: ", templates

broker_kwargs = build_broker_kwargs(
    broker_config,
    settings.GEOWATCH_CONFIG,
    verbose=verbose)
broker_kwargs["templates"] = templates
#print "##############"
#print "KWARGS: ", broker_kwargs

broker = SlackBotOSMBroker(
    broker_config.get('name', None),
    broker_config.get('description', None),
    **broker_kwargs)
broker.run(run_cycle_out=False)  # run_cycle_out=False prevents default producer behavior
