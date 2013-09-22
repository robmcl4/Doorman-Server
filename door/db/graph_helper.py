from door.db.connection import get_conn

def _fill_times(arr, to_fill):
    """
        Fill in times in arr with that from to_fill

        arr: [[TIME-int, 0], ...]
        to_fill: [[TIME-int, int] ...]

        returns:
          [['12AM', 3], ...]
    """
    for hour, count in to_fill:
        arr[arr.index([hour, 0])] = [hour, count]

    # format the first of ret to be a readable time
    def fmt(n):
        ampm = "AM" if n < 12 else "PM"
        n %= 12
        if n == 0:
            n = 12
        return "{0}{1}".format(n, ampm)
    for i in range(len(arr)):
        arr[i] = [fmt(arr[i][0]), arr[i][1]]

def daily_summary():
    """
        Returns [['TIME', opens], ...]
    """
    conn = get_conn()
    curs = conn.cursor()
    curs.execute("""
      select hour(ts) as hr, count(*) as num 
      from events 
      where DATE(ts) = DATE(NOW()) 
            and type='open'
      group by hr
    """)

    # make sure every hour is accounted for, so start with all zero'd and then set the numbers
    ret = [[x, 0] for x in range(24)]
    _fill_times(ret, curs.fetchall())

    curs.close()
    return ret

def daily_total_summary():
    """
        Returns [['TIME', opens], ...]
    """
    conn = get_conn()
    curs = conn.cursor()
    curs.execute("""
      select hour(ts) as hr, count(*) as num
      from events
      where type = 'open'
      group by hr
    """)
    ret = [[x, 0] for x in range(24)]
    _fill_times(ret, curs.fetchall())

    curs.close()
    return ret

def _pad_weekly(points):
    """
        Return an array of points that are padded (so days with no points are in there as zeros)
        
        points: [['Monday-18', 4], ...]
        returns: [['Monday-6PM', 4], ['Tuesday-12AM', 0] ...]
    """
    # format empty return values
    ret = []
    for x in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
        for n in ['12PM', '6AM', '12AM', '6PM']:
            ret.append([x + '-' + n, 0])
    
    # format the values from sql and put them into the ret array
    for wkday, num in points:
        split = wkday.split('-')
        n = int(split[1])
        ampm = 'AM' if n < 12 else 'PM'
        n %= 12
        if n==0: n = 12
        new_wkday = split[0] + '-' + str(n) + ampm
        new_point = [new_wkday, num]
        ret[ret.index([new_wkday, 0])] = new_point
    return ret

def weekly_summary():
    """
        Returns [['MONDAY-12AM', 12], ...]
    """
    conn = get_conn()
    curs = conn.cursor()
    curs.execute("""
       select 
         concat(dayname(ts), '-', (hour(ts) div 6)*6) as wkday,
         count(*) as num
       from events
       where type = 'open' and week(ts) = week(now()) and year(ts) = year(now())
       group by wkday
    """)
    ret = _pad_weekly(curs.fetchall())
    curs.close()
    return ret

def weekly_total_summary():
    """
        Returns [['MONDAY-12AM', 12], ...]
    """
    conn = get_conn()
    curs = conn.cursor()
    curs.execute("""
       select 
         concat(dayname(ts), '-', (hour(ts) div 6)*6) as wkday,
         count(*) as num
       from events
       where type = 'open'
       group by wkday
    """)
    ret = _pad_weekly(curs.fetchall())
    curs.close()
    return ret
