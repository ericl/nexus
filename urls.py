from django.conf.urls.defaults import *
from django.conf import settings
from django.views.decorators.cache import never_cache
from django.http import HttpResponse
from cover.views import *
from archive.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^nexus/', include('nexus.foo.urls')),

    # Uncomment the next line to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line for to enable the admin:
    (r'^admin/(.*)', admin.site.root),


    (r'^$', frontpage),
    (r'^test$', never_cache(frontpage)),
    (r'^null/', lambda x: HttpResponse('')),
    (r'^ajax/embed/(\d{4})/(\d{2})/([-_a-zA-Z0-9]+)/$', articlepage),
    (r'^ajax/embed/author/([-_a-zA-Z0-9]+)$', authorpage),
    (r'^ajax/embed/image/([-_a-zA-Z0-9]+)/$', imageview),
    (r'^ajax/embed/tag/([-_a-zA-Z0-9]+)$', tagpage),
    (r'^ajax/embed/info/staff$', staff_auto_infopage),
    (r'^ajax/embed/info/([-_a-zA-Z0-9]+)$', infopage),
    (r'^ajax/embed/static/([-_a-zA-Z0-9]+)$', staticpage),
    (r'^ajax/embed/polls$', pollpage),
    (r'^ajax/embed/poll_history$', pollhist),
    (r'^ajax/embed/archive/$', issue_gallery),
    (r'^ajax/embed/archive/current/$', current_page_gallery),
    (r'^ajax/embed/archive/(\d{4}-\d{2}-\d{2})/$', page_gallery),
    (r'^ajax/paginator$', paginate),
    (r'^ajax/poll/$', poll_results),

    (r'^(\d{4})/(\d{2})/([-_a-zA-Z0-9]+)/$', wrap(articlepage)),
    (r'^image/([-_a-zA-Z0-9]+)/$', wrap(imageview)),
    (r'^tag/([-_a-zA-Z0-9]+)$', wrap(tagpage)),
    (r'^author/([-_a-zA-Z0-9]+)$', wrap(authorpage)),
    (r'^info/staff$', wrap(staff_auto_infopage)),
    (r'^info/([-_a-zA-Z0-9]+)$', wrap(infopage)),
    (r'^static/([-_a-zA-Z0-9]+)$', wrap(staticpage)),
    (r'^polls$', wrap(pollpage)),
    (r'^poll_history$', wrap(pollhist)),
    (r'^archive/$', wrap(issue_gallery)),
    (r'^archive/current/$', wrap(current_page_gallery)),
    (r'^archive/(\d{4}-\d{2}-\d{2})/$', wrap(page_gallery)),

    (r'^test/(\d{4})/(\d{2})/([-_a-zA-Z0-9]+).*$', test(articlepage)),
    (r'^test/image/([-_a-zA-Z0-9]+).*$', test(imageview)),
    (r'^test/tag/([-_a-zA-Z0-9]+).*$', test(tagpage)),
    (r'^test/author/([-_a-zA-Z0-9]+).*$', test(authorpage)),
    (r'^test/info/staff.*$', test(staff_auto_infopage)),
    (r'^test/info/([-_a-zA-Z0-9]+).*$', test(infopage)),
    (r'^test/static/([-_a-zA-Z0-9]+).*$', test(staticpage)),
    (r'^test/polls.*$', test(pollpage)),
    (r'^test/poll_history.*$', test(pollhist)),
    (r'^test/archive/(\d{4}-\d{2}-\d{2}).*$', test(page_gallery)),
    (r'^test/archive/current.*$', test(current_page_gallery)),
    (r'^test/archive.*$', test(issue_gallery)),
)
if settings.DEBUG: # not in production!
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
