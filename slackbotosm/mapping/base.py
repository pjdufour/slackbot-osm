from geowatchutil.mapping.base import GeoWatchMapping

from slackbotosm import settings

from slackbotosm.enumerations import URL_PROJECT_VIEW, URL_PROJECT_EDIT, URL_PROJECT_TASKS, URL_CHANGESET_VIEW, URL_USER_VIEW, TASK_STATE_READY, TASK_STATE_INVALIDATED, TASK_STATE_DONE, TASK_STATE_VALIDATED, TASK_STATE_REMOVED


class GeoWatchMappingProject(GeoWatchMapping):

    def forward(self, **kwargs):
        project = kwargs.get("project", None)
        counter = kwargs.get("counter", None)
        message = {
            "title": "HOT Project "+str(project),
            "project": str(project),
            "url_view": URL_PROJECT_VIEW.format(project=project),
            "url_edit": URL_PROJECT_EDIT.format(project=project),
            "url_tasks": URL_PROJECT_TASKS.format(project=project),
            "count_ready": counter[str(TASK_STATE_READY)],
            "count_invalidated": counter[str(TASK_STATE_INVALIDATED)],
            "count_done": counter[str(TASK_STATE_DONE)],
            "count_validated": counter[str(TASK_STATE_VALIDATED)],
            "count_removed": counter[str(TASK_STATE_REMOVED)]
        }
        total = message["count_done"] + message["count_ready"] + message["count_validated"] + message["count_invalidated"]
        message["percent"] = 100.0 * (message["count_done"] + message["count_validated"]) / total

        return message

    def __init__(self):
        super(GeoWatchMappingProject, self).__init__()


class GeoWatchMappingChangeset(GeoWatchMapping):

    def forward(self, **kwargs):
        id = kwargs.get("id", -1)
        message = {
            "title": "OSM Changeset "+str(id),
            "changeset": str(id),
            "date": kwargs.get("closed_at", ""),
            "imagery": kwargs.get("imagery_used", "unknown"),
            "comment": kwargs.get("comment", ""),
            "user": kwargs.get("user", ""),
            "url_changeset_view": URL_CHANGESET_VIEW.format(changeset=id),
            "url_user_view": URL_USER_VIEW.format(user=kwargs.get("user",""))
        }
        return message

    def __init__(self):
        super(GeoWatchMappingChangeset, self).__init__()
