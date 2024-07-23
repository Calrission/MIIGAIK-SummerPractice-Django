from django.contrib import admin
from django.urls import path, include

from blog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls', namespace='blog')),
    path('account/', include('account.urls', namespace="account")),
    path('', views.post_list),
]
