import os
from pyramid.config import Configurator
from pyramid.settings import asbool

#from pyramid_angularjs_starter.views import my_view

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

    # add html renderer (chameleon based)
    config.add_renderer(name='.html', factory='pyramid_angularjs_starter.renderer.AppDistRendererFactory')

    production_config = asbool(settings.get('PRODUCTION', 'false'))
    production_config = asbool(settings.get('PRODUCTION', 'false'))
    production = os.environ.get('PRODUCTION', production_config)
    minify_config = settings.get('minify', 'app')
    minify = os.environ.get('minify', minify_config)
    config.include('pyramid_chameleon')

    # static views
    # See also config.override_asset if you want to avoid minify
    config.add_static_view('scripts', 'pyramid_angularjs_starter:webapp/%s/scripts' % minify, cache_max_age=3600)
    config.add_static_view('styles', 'pyramid_angularjs_starter:webapp/%s/styles' % minify, cache_max_age=3600)
    config.add_static_view('images', 'pyramid_angularjs_starter:webapp/%s/images' % minify, cache_max_age=3600)
    if not production:
        # we expose the bower_components dir just for development deployments, not good for production
        config.add_static_view('bower_components', 'pyramid_angularjs_starter:webapp/%s/bower_components' % minify, cache_max_age=3600)

    # routes
    config.add_route('home', '/')

    config.scan()
    return config.make_wsgi_app()
