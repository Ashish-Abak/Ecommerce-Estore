from django.contrib import admin
from django.urls import path
from ecommapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home',views.home),
    path('all',views.all),
    path('catfilter/<cv>',views.catfilter),
    path('range',views.range),
    path('sort/<sv>',views.sort),
    path('pd/<pid>',views.pd),
    path('login',views.login_user),
    path('logout',views.logout_user),
    path('Cart',views.Cart),
    path('remove/<cid>',views.remove),
    path('removes/<oid>',views.removes),    
    path('updateqty/<qv>/<cid>',views.updateqty),
    path('placeorder',views.placeorder),
    path('makepayment',views.makepayment),
    path('sendmail',views.sendmail),
    path('contact',views.contact),
    path('about',views.about),
    path('addtocart/<pid>',views.addtocart),
    path('registration',views.registration),


]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)