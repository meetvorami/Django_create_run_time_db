from django.urls import path

from .views import EmployeeApiVieW

urlpatterns = [
    path("<str:org_name>/employees/", EmployeeApiVieW.as_view(), name="list_employees"),
]
