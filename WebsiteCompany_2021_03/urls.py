"""WebsiteCompany_2021_03 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from Operator.views import adminView, frontView, logged_out, staff_in, customer_in, shipment_print, mainView1, mainView2
import notifications.urls
from django.conf.urls import url
from django.conf.urls import include

urlpatterns = [
    #    path('admin/', admin.site.urls),
    
    path('administration/', adminView, name="adminPage"),
    path('', frontView, name="frontpage"),
    path('staff_in/', staff_in, name="staff_redirect"),
    path('customer_in/', customer_in, name="customer_redirect"),
    url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
    path('logged_out/', logged_out, name="logged_out"),
    path('main_page_staff/', mainView1, name="mainPage1"),
    path('main_page_customer/', mainView2, name="mainPage2"),
    path('shipment_printing/', shipment_print, name="shipment_print"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
