"""
WSGI config for student_be project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.student_be.settings")

application = get_wsgi_application()
