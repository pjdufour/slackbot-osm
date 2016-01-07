SLACK_MESSAGE_TEMPLATE_PROJECT = {
    "attachments": [{
        "title": "{title}",
        "title_link": "{url_view}",
        "fallback": "Project {project} has the following counts: {count_ready} ready, {count_invalidated} invalidated, {count_done} done, {count_validated} validated, {count_removed} removed.",
        "text": "Project <{url_view}|{project}> has the following counts: {count_ready} ready, {count_invalidated} invalidated, {count_done} done, {count_validated} validated, {count_removed} removed.",
        "fields": [{
            "title": "View Project",
            "value": "<{url_view}|View>",
            "short": True
        },
        {
            "title": "Edit Project Settings",
            "value": "<{url_edit}|Edit>",
            "short": True
        },
        {
            "title": "Download GeoJSON of Tasks",
            "value": "<{url_tasks}|Download>",
            "short": True
        }],
        "color": "#000099"
    }]
}
