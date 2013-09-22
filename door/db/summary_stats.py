"""
  summary_stats.py
  
  Contains summary statistics from the door database.

  Author: Robert McLaughlin
"""

from door.db.connection import get_conn

TIMEOUT = 3*60 # the timeout of heartbeats in seconds

ONLINE, OFFLINE, OPEN, CLOSED, UNKNOWN = range(5)

def total_opens():
    """
        Get the total numbner of opens as an integer
    """
    conn = get_conn()
    curs = conn.cursor()
    curs.execute("select count(*) from events where type = %s", ("open",))
    ret = curs.fetchone()[0]
    curs.close()
    return ret

def get_online_status():
    """
        Get the online/offline status of the door
        returns:
            summary_stats.ONLINE or summary_stats.OFFLINE
    """
    conn = get_conn()
    curs = conn.cursor()
    curs.execute("select TIME_TO_SEC(timediff(NOW(), last)) < %s as diff from heartbeat", (TIMEOUT,))
    ret = curs.fetchone()[0]
    ret = ONLINE if ret == 1 else OFFLINE
    curs.close()
    return ret

def get_open_status():
    """
        Get the open/closed status of the door based on the last
        entry in the sql table
        returns:
            summary_stats.OPEN or summary_stats.CLOSED
            or
            summary_stats.UNKNOWN if offline
    """
    conn = get_conn()
    curs = conn.cursor()
    curs.execute("select type from events order by ts desc limit 1")
    ret = curs.fetchall()
    ret = (OPEN if ret[0][0].lower() == 'open' else CLOSED) if len(ret) else UNKNOWN
    curs.close()
    return ret

def get_opens_today():
    """
        Get an integer for how many opens occurred in the past 24 hrs
    """
    conn = get_conn()
    curs = conn.cursor()
    curs.execute("select count(*) from events where type = 'open' and DATE(ts) = DATE(NOW())")
    ret = curs.fetchone()[0]
    curs.close()
    return ret

def get_opens_weekly():
    """
        Get an integer for how many opens occurred this week
        (this number rolls over to zero at the end of the week)
    """
    conn = get_conn()
    curs = conn.cursor()
    curs.execute("select count(*) from events where type = 'open' and week(ts) = week(now()) and year(ts) = year(now())")
    ret = curs.fetchone()[0]
    curs.close()
    return ret

def get_daily_stddev():
    """
        Get the standard deviation of an open for the day
    """
    conn = get_conn()
    curs = conn.cursor()
    curs.execute("select stddev(tbl.num) from (select count(*) as num from events where type = 'open' group by DATE(ts)) as tbl")
    ret = curs.fetchone()[0]
    curs.close()
    ret = round(float(ret), 3)
    return ret

def get_daily_avg():
    """
        Get the average number of opens per day
    """
    conn = get_conn()
    curs = conn.cursor()
    curs.execute("select avg(tbl.num) from (select count(*) as num from events where type = 'open' group by DATE(ts)) as tbl")
    ret = curs.fetchone()[0]
    curs.close()
    ret = round(float(ret), 3)
    return ret
