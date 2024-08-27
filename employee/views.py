from rest_framework.response import Response
from rest_framework.views import APIView, status

from employee.models import Employee
from employee.serializer import EmployeeListSerialzer


class EmployeeApiVieW(APIView):
    def get(self, request, org_name):
        ememployees = Employee.objects.using(org_name).all()
        serializer_class = EmployeeListSerialzer(ememployees, many=True)
        return Response({"data": serializer_class.data}, status=status.HTTP_200_OK)

    def post(self, request, org_name):
        if (
            Employee.objects.using(org_name)
            .filter(email=request.data.get("email"))
            .exists()
        ):
            return Response({"message": "user already exist with that email"})
        serializer_class = EmployeeListSerialzer(data=request.data)
        serializer_class.is_valid()
        validated_data = serializer_class.validated_data
        employee = Employee.objects.using(org_name).create(**validated_data)
        serializer_class = EmployeeListSerialzer(employee)
        return Response(
            {"status": "Employee created successfully", "data": serializer_class.data},
            status=201,
        )
