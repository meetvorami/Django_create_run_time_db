from django.conf import settings

from .middleware import ThreadLocalDBConfig


class DatabaseRouter:
    def db_for_read(self, model, **hints):
        return self.get_db_alias()

    def db_for_write(self, model, **hints):
        return self.get_db_alias()

    def get_db_alias(self):
        db_config = ThreadLocalDBConfig.get_db_config()
        if db_config:
            alias = self.find_database_alias(db_config)
            if alias:
                return alias
        return "default"

    def find_database_alias(self, db_config):
        for alias, config in settings.DATABASES.items():
            config_filtered = {k: config[k] for k in db_config if k in config}
            db_config_filtered = {k: db_config[k] for k in config_filtered}
            if config_filtered == db_config_filtered:
                return alias

        return None
