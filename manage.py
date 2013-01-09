#!/usr/bin/env python
import os
import sys

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

if __name__ == "__main__":
    sys.path.insert(0, os.path.join(PROJECT_PATH, 'store'))
    sys.path.insert(0, os.path.join(PROJECT_PATH, 'extensions'))

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "store.settings")
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
