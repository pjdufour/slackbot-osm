import json
import re

from geowatchutil.base import GeoWatchError
from geowatchutil.broker.base import GeoWatchBroker
from geowatchutil.codec.geowatch_codec_slack import GeoWatchCodecSlack

from slackbotosm.enumerations import URL_PROJECT_VIEW, URL_PROJECT_EDIT, URL_PROJECT_TASKS
from slackbotosm.mapping.base import GeoWatchMappingProject
from slackbotosm.utils import load_patterns

class SlackBotOSMBroker(GeoWatchBroker):
    """
    Broker for Slack Bot for OpenStreetMap
    """
    _user_id = None  # Dervied from consumer authtoken
    _user_name = None  # Dervied from consumer authtoken
    patterns = None

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
                msgsubtype = m.get(u'subtype', None)
                if msgsubtype == u'bot_message':
                    username = m[u'username']
                    text = m[u'text']
                    pass
                elif msgsubtype == u'message_deleted':
                    pass
                else:
                    user = m[u'user']
                    text = m[u'text']
                    channel = m[u'channel']

                    print "testing Message", m
                    match_question = None
                    match_value = None
                    for question in self.patterns:
                        for pattern in self.patterns[question]:
                            match_value = re.search(pattern, text, re.M|re.I)
                            if match_value:
                                match_question = question
                                break
                        if match_value:
                            break

                    if match_value:
                        outgoing = None
                        print "Match Question: ", match_question
                        print "Match Value: ", match_value
                        if match_question == "project":
                            try:
                                ctx = self._request_project(match_value.group("project"))
                                t = self.templates.get('SLACK_MESSAGE_TEMPLATE_PROJECT', None)
                                if t:
                                    outgoing = self.codec_slack.render(ctx, t=t)
                            except:
                                print "Error processing match for original text: ", text
                        elif match_question == "user":
                            pass

                        if outgoing:
                            print "Sending message ..."
                            print "+ Data = ", outgoing
                            self.duplex[0]._channel.send_message(outgoing, topic=channel)


    def _request_project(self, project):

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

        return GeoWatchMappingProject().forward(project=int(project), counter=counter)

    def _req_user(self, messages):
        passs

    def __init__(self, name, description, templates=None, duplex=None, consumers=None, producers=None, stores_out=None, filter_metadata=None, sleep_period=5, count=1, timeout=5, deduplicate=False, verbose=False):  # noqa
        super(SlackBotOSMBroker, self).__init__(
            name,
            description,
            duplex=duplex,
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

        self.templates = templates  # loaded from templates.yml
        self._user_id = self.duplex[0]._client._user_id
        self._user_name = self.duplex[0]._client._user_name

        self.codec_slack = GeoWatchCodecSlack()

        self.patterns = load_patterns()
