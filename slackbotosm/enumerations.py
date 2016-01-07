PATTERN_PROJECT = "^([<][@]\w+[>])(\s+)(project)(\s+)(?P<project>\d+)$"
PATTERN_USER = "^([<][@]\w+[>])(\s+)(user)(\s+)(?P<user>\w+)$"

URL_PROJECT_VIEW="http://tasks.hotosm.org/project/{project}"
URL_PROJECT_EDIT="http://tasks.hotosm.org/project/{project}/edit"
URL_PROJECT_TASKS="http://tasks.hotosm.org/project/{project}/tasks.json"

TASK_STATE_READY = 0
TASK_STATE_INVALIDATED = 1
TASK_STATE_DONE = 2
TASK_STATE_VALIDATED = 3
TASK_STATE_REMOVED = -1

