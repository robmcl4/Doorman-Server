import sys
import os

_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not _path in sys.path:
    sys.path.append(_path)

from door.pages import *
