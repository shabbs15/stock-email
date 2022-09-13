from django.conf.urls import handler404
from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('stocks.urls'))
]

handler404 = 'stocks.views.pageNotFound'
