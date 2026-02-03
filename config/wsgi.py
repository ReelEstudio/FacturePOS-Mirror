import os
import subprocess
import sys

# Intentar encontrar la ruta de las librerías de Nix dinámicamente
try:
    nix_lib_path = subprocess.check_output(['nix-build', '-E', 'with import <nixpkgs> {}; symlinkJoin { name = "libs"; paths = [ pango cairo glib ]; }', '--no-out-link']).decode().strip() + "/lib"
    if nix_lib_path not in os.environ.get('LD_LIBRARY_PATH', ''):
        os.environ['LD_LIBRARY_PATH'] = f"{nix_lib_path}:{os.environ.get('LD_LIBRARY_PATH', '')}"
except:
    # Si falla lo anterior, usamos la ruta estándar de perfiles de Nixpacks
    os.environ['LD_LIBRARY_PATH'] = f"/nix/var/nix/profiles/default/lib:{os.environ.get('LD_LIBRARY_PATH', '')}"

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

"""
WSGI config for web project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
