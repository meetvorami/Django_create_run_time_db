from .models import Employee
from rest_framework.serializers import ModelSerializer

class EmployeeListSerialzer(ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'  
