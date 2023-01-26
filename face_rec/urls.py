from django.urls import path,include,re_path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

from FYP_Interface import settings
urlpatterns = [
    path('',views.Login, name='login'),
    path('logout/',views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('home/', views.home, name='home'),
    path('new/', views.newis, name='new'),
    path('enroll/', views.enroll_new, name='enroll'),
    path('viewall/', views.viewall, name='viewall'),
    path('about/', views.about_us, name='about'),
    path('contact/',views.contact,name='contact'),
    re_path(r'^delete/(?P<auth_id>[0-9]+)$', views.delete, name='delete'),


]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
