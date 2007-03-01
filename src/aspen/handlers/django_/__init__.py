"""This package provides WSGI apps for serving Django w/o urlconf madness.

The two apps:

  script        execs PATH_TRANSLATED as a Python script

  template      renders PATH_TRANSLATED as a Django template


The namespace for each is an extended Django RenderContext:

  http://www.djangobook.com/en/beta/chapter10/#cn62


The additional keys are:

  __file__      equivalent to PATH_TRANSLATED
  http          the django.http module [scripts only]
  request       the current Django HttpRequest object
  response      a Django HttpResponse object [scripts only]


Our main class here is wsgi.WSGI, a thin wrapper around BaseHandler.get_response
(WSGIHandler doesn't define the method), which hacks request.urlconf to use the
filesystem for site hierarchy rather than the settings module. Since Django
finds an urlconf based on a magic name within a module ('urlpatterns'), we need
a separate module for each type of file: script and template. That's the reason
for the layout of this package.

"""
# the imports are relative to support use outside aspen

try:
    import django
except ImportError:
    def wsgi(environ, start_response):
        # This should probably raise at import time, but that would take more
        # work to not trigger in tests.
        raise NotImplementedError("django is not on PYTHONPATH")
    script = template = wsgi
else:
    from _script import wsgi as script
    from _template import wsgi as template

__all__ = ['script', 'template']