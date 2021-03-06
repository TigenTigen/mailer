from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('user.urls', namespace='user')),
    path('', include('core.urls', namespace='core')),
]
