import json
import re

from geowatchutil.base import GeoWatchError
from geowatchutil.broker.base import GeoWatchBroker
from geowatchutil.codec.geowatch_codec_slack import GeoWatchCodecSlack

from slackbotosm import templates
from slackbotosm.enumerations import PATTERN_PROJECT, PATTERN_USER, URL_PROJECT_VIEW, URL_PROJECT_EDIT, URL_PROJECT_TASKS
from slackbotosm.mapping.base import GeoWatchMappingProject

class SlackBotOSMBroker(GeoWatchBroker):
    """
    Broker for Slack Bot for OpenStreetMap
    """
    _user_id = None  # Dervied from consumer authtoken
    _user_name = None  # Dervied from consumer authtoken

    def _make_request(self, url, params=None, data=None, cookie=None, contentType=None):
        """
        Prepares a request from a url, params, and optionally authentication.
        """

        import urllib
        import urllib2

        if params:
            url = url + '?' + urllib.urlencode(params)

        req = urllib2.Request(url, data=data)

        if cookie:
            req.add_header('Cookie', cookie)

        if contentType:
            req.add_header('Content-type', contentType)
        else:
            if data:
                req.add_header('Content-type', 'text/xml')

        return urllib2.urlopen(req)

    def _pre(self):
        pass

    def _post(self, messages=None):
        for m in messages:
            msgtype = m[u'type']
            if msgtype == u'hello':  # slack always open up connection with hello message
                pass
            elif msgtype == u'message':
                user = m[u'user']
                text = m[u'text']
                channel = m[u'channel']
                
                print "testing Message", m
                if text.startswith("<@"+self._user_id+">"):
                    match = re.match(PATTERN_PROJECT, text)
                    if match:
                        self._req_project(match.group("project"))
                    else:
                        match = re.match(PATTERN_USER, text)
                        #if match:
                        #    self._req_user(m)

    def _req_project(self, project):

        url = URL_PROJECT_TASKS.format(project=project)
        request = self._make_request(url, contentType="application/json")

        if request.getcode () != 200:
            raise Exception("Could not fetch json for project "+project+".")

        response = request.read()
        data = json.loads(response)

        counter = {
            "0": 0,
            "1": 0,
            "2": 0,
            "3": 0,
            "-1": 0
        }
        for f in data[u'features']:
            p = f[u'properties']
            state = str(p.get(u'state', None))
            counter[state] = counter[state] + 1

        ctx = GeoWatchMappingProject().forward(project=int(project), counter=counter)
        t = getattr(templates, 'SLACK_MESSAGE_TEMPLATE_PROJECT')
        data = self.codec_slack.render(ctx, t=t)
        self.consumers[0]._channel.send_message(data)

    def _req_user(self, messages):
        pass

    def __init__(self, name, description, consumers=None, filter_metadata=None, producers=None, stores_out=None, sleep_period=5, count=1, timeout=5, deduplicate=False, verbose=False):  # noqa
        super(SlackBotOSMBroker, self).__init__(
            name,
            description,
            consumers=consumers,
            producers=producers,
            stores_out=stores_out,
            count=count,
            threads=1,
            sleep_period=sleep_period,
            timeout=timeout,
            deduplicate=deduplicate,
            filter_metadata=filter_metadata,
            verbose=verbose)

        self._user_id = self.consumers[0]._client._user_id
        self._user_name = self.consumers[0]._client._user_name

        self.codec_slack = GeoWatchCodecSlack(templates=templates)
