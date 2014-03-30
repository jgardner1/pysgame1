"""Miscellaneous things that don't really belong anywhere."""
import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def clamp(bottom, top, value):
    """Returns value clamped between bottom and top."""
    assert bottom < top
    return max(bottom, min(top, value))


