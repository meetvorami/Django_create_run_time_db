from django.http import JsonResponse
from .models import Organization

from django.core.management import call_command
from django.db import connections
from django.views.decorators.csrf import csrf_exempt


import psycopg2  

@csrf_exempt
def register_organization(request):
    if request.method == 'POST':
        org_name = request.POST.get('name')
        db_name = request.POST.get('db_name')
        db_user = request.POST.get('db_user')
        db_password = request.POST.get('db_password')
        db_host = request.POST.get('db_host')
        db_port = request.POST.get('db_port')
        db_engine  = request.POST.get("db_engine")

        if not Organization.objects.filter(name=org_name).exists():
            Organization.objects.create(
                name=org_name,
                db_name=db_name,
                db_user=db_user,
                db_password=db_password,
                db_host=db_host,
                db_port=db_port,
                db_engine=db_engine
            )

            # Define the new database connection settings
            new_db_settings = {
                'ENGINE': db_engine,
                'NAME': db_name,
                'USER': db_user,
                'PASSWORD': db_password,
                'HOST': db_host,
                'PORT': db_port,
                'OPTIONS': {},
                'TIME_ZONE': 'UTC',
                'ATOMIC_REQUESTS': True,
                'CONN_HEALTH_CHECKS': True,
                'CONN_MAX_AGE': 600,  
                'AUTOCOMMIT': True, 
            }

            # Register the new connection
            connections.databases[org_name] = new_db_settings

            # Create the new database
        
            # Connect to the PostgreSQL server (not to a specific database)
            connection = psycopg2.connect(
                dbname='postgres',
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port
            )
            connection.autocommit = True
            cursor = connection.cursor()
            cursor.execute(f"CREATE DATABASE {db_name};")

            call_command('migrate',app_label="employee", database=org_name)
            return JsonResponse({'status': 'Organization registered and database migrated successfully'})
        else:
            return JsonResponse({'status': 'Organization already exists'})
    return JsonResponse({'status': 'Invalid request method'}, status=405)