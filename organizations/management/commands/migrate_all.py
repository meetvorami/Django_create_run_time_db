from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connections
from organizations.models import Organization  # Import your Organization model

class Command(BaseCommand):
    help = 'Apply migrations to all registered organization databases'

    def handle(self, *args, **options):
        # Fetch all registered organizations
        organizations = Organization.objects.all()
        
        for org in organizations:
            db_settings = {
                'ENGINE': 'django.db.backends.postgresql',  # Adjust as needed
                'NAME': org.db_name,
                'USER': org.db_user,
                'PASSWORD': org.db_password,
                'HOST': org.db_host,
                'PORT': org.db_port,
                'OPTIONS': {},
                'TIME_ZONE': 'UTC',
                'ATOMIC_REQUESTS': True,
                'CONN_HEALTH_CHECKS': True, 
                'CONN_MAX_AGE': 600,  # Max age of database connections (in seconds)
                'AUTOCOMMIT': True,'options':{}
            }
            
            # Register the new connection settings
            connections.databases[org.name] = db_settings
            
            # Apply migrations for the specific database
            self.stdout.write(f'Applying migrations for database: {org.name}')
            try:
                call_command('migrate', database=org.name)
                self.stdout.write(self.style.SUCCESS(f'Successfully migrated database: {org.name}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error migrating database: {org.name} - {str(e)}'))
