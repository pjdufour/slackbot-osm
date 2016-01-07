from geowatchutil.base import GeoWatchError
from geowatchutil.broker.base import GeoWatchBroker

from slackbotosm.enumerations import MSG_START, PATTERN_PROJECT, PATTERN_USER, URL_PROJECT

class SlackBotOSMBroker(GeoWatchBroker):
    """
    Broker for Slack Bot for OpenStreetMap
    """

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
                if text.startswith(MSG_START):
                    match = re.match(PATTERN_PROJECT, text)
                    if match:
                        self._req_project(match.group(3))
                    else:
                        match = re.match(PATTERN_USER, text)
                        #if match:
                        #    self._req_user(m)

    def _req_project(self, project):

        url = URL_PROJECT.format(project=project)
        request = self._make_request(url, contentType="application/json")

        if request.getcode () != 200:
            raise Exception("Could not fetch json for project "+project+".")

        response = request.read()
        data = json.loads(response)
        print data

        # Use templates to build new message
        # Have slack client/channel send back to original slack

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
