"""
  connection.py
  
  Manages and holds a connection to the database
"""

from mysql import connector
import threading
from door.config import config
import os
import logging

_path = os.path.dirname(os.path.abspath(__file__))
_key_dir = os.path.join(_path, "ssl")

_local = threading.local()

def _connect():
    """
        Connects to the database using the door.config information
    """
    global _local
    
    if hasattr(_local, 'conn') and _local.conn:
        try:
            _local.conn.close()
        except:
            pass

    section = config['mysql']

    user  = section['user']
    pass_ = section['pass']
    db    = section['database']
    host  = section['host']
    port  = section['port']
    
    ssl_options = {}
    if section['ssl'].strip().lower() == 'true':
        ssl_options['ssl_ca']   = os.path.join(_key_dir, "ca-cert.pem")
        ssl_options['ssl_cert'] = os.path.join(_key_dir, "client-cert.pem")
        ssl_options['ssl_key']  = os.path.join(_key_dir, "client-key.pem")
        ssl_options['ssl_verify_cert'] = True

    _local.conn = connector.connect(user=user,
                              passwd=pass_,
                              db=db,
                              host=host,
                              port=port,
                              **ssl_options)

def get_conn():
    if not hasattr(_local, 'conn') or not _local.conn:
        _connect()
    if not _local.conn.is_connected():
        _local.conn.reconnect()
    _local.conn.commit()
    return _local.conn
