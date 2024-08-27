from django.apps import apps
from django.db import connections
from django.utils.deprecation import MiddlewareMixin


class DatabaseRouterMiddleware(MiddlewareMixin):
    def process_request(self, request):
        path = request.path.strip("/").split("/")
        if path:
            org_name = path[0]
            try:
                Organization = apps.get_model("organizations", "Organization")
                organization = Organization.objects.get(name=org_name)
                if org_name not in connections.databases:
                    connections.databases[org_name] = {
                        "ENGINE": organization.db_engine,
                        "NAME": organization.db_name,
                        "USER": organization.db_user,
                        "PASSWORD": organization.db_password,
                        "HOST": organization.db_host,
                        "PORT": organization.db_port,
                        "OPTIONS": {},
                        "TIME_ZONE": "UTC",
                        "ATOMIC_REQUESTS": True,
                        "CONN_HEALTH_CHECKS": True,
                        "CONN_MAX_AGE": 600,
                        "AUTOCOMMIT": True,
                    }

            except Organization.DoesNotExist:
                pass
