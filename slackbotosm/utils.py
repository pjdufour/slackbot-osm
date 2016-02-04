import yaml


def load_patterns():
    patterns = None
    with open("slackbotosm/patterns.yml", 'r') as f:
        try:
            patterns = yaml.load(f)
        except:
            raise
    return patterns


def load_templates():
    templates = None
    with open("slackbotosm/templates.yml", 'r') as f:
        try:
            templates = yaml.load(f)
        except:
            pass
    return templates
