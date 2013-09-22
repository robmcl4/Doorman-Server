import cherrypy
from chameleon import PageTemplateLoader as Loader
import os
from door.db import summary_stats, graph_helper
import json

_path = os.path.dirname(os.path.abspath(__file__))
_template_path = os.path.join(_path, 'templates')

_templates = Loader(_template_path)

def template(template_name):
    def new_wrapper(func):
        def wrapper():
            ret = func()
            return _templates[template_name](**ret)
        wrapper.exposed = True
        return wrapper
    return new_wrapper

def json_page(func):
    def new_func():
        ret = func()
        return json.dumps(ret)
    new_func.exposed = True
    return new_func

@template("index.pt")
def index():
    ret = {}
    ret['total_opens'] = summary_stats.total_opens()
    if summary_stats.get_open_status() == summary_stats.OPEN:
        ret['open_status'] = "Open"
    else:
        ret['open_status'] = "Closed"
    ret['online'] = summary_stats.get_online_status() == summary_stats.ONLINE
    ret['daily_opens'] = summary_stats.get_opens_today()
    ret['weekly_opens'] = summary_stats.get_opens_weekly()
    ret['daily_stddev'] = summary_stats.get_daily_stddev()
    ret['daily_mean'] = summary_stats.get_daily_avg()
    return ret

@json_page
def daily_summary():
    return graph_helper.daily_summary()

@json_page
def daily_total_summary():
    return graph_helper.daily_total_summary()

@json_page
def weekly_summary():
    return graph_helper.weekly_summary()

@json_page
def weekly_total_summary():
    return graph_helper.weekly_total_summary()
