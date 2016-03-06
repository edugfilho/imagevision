"""
`appengine_config.py` is automatically loaded when Google App Engine
starts a new instance of your application. This runs before any
WSGI applications specified in app.yaml are loaded.
"""

from google.appengine.ext import vendor

# Third-party libraries are stored in "lib", vendoring will make
# sure that they are importable by the application.
vendor.add('lib')

# Trick to make _ssl work on devserver: http://stackoverflow.com/a/31955446/4402547
import os

if os.environ.get('SERVER_SOFTWARE', '').startswith('Development'):
    import imp
    import os.path
    import inspect
    from google.appengine.tools.devappserver2.python import sandbox

    sandbox._WHITE_LIST_C_MODULES += ['_ssl', '_socket']
    # Use the system socket.

    real_os_src_path = os.path.realpath(inspect.getsourcefile(os))
    psocket = os.path.join(os.path.dirname(real_os_src_path), 'socket.py')
    imp.load_source('socket', psocket)