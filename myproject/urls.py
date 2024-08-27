from django.contrib import admin
from django.urls import path, include
from organizations.views import register_organization

urlpatterns = [
    
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register_organization, name='register_organization'),
    path('', include('employee.urls')),

]
