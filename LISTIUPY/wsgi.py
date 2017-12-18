"""
WSGI config for LISTIUPY project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import sys
apache_configuration= os.path.dirname(__file__)  
project = os.path.dirname(apache_configuration)  
workspace = os.path.dirname(project)  

sys.path.append(project)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LISTIUPY.settings")

application = get_wsgi_application()
