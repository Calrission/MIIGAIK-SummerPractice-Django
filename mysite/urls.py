from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from blog.views import post_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls', namespace='blog')),
    path('account/', include('account_site.urls', namespace='account_site')),
    path('', post_list, name='blog-home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
