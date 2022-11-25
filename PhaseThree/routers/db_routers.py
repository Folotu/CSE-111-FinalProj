from django.http import Http404
from ecommerce import settings 

class inciteRouter:
    """
    A router to control all database operations on models in the
    auth and contenttypes applications.
    """
    # route_app_labels = {'auth', 'contenttypes', 'admin', 'sessions', 'invent' }
    # route_app_labels = {'auth', 'contenttypes', 'admin','sessions', 'store'}
    route_app_labels = {'auth', 'contenttypes', 'admin', 'sessions', 'incite' }

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth and contenttypes models go to default.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'default'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth and contenttypes models go to default.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'default'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth or contenttypes apps is
        involved.
        """
        if (
            obj1._meta.app_label in self.route_app_labels or
            obj2._meta.app_label in self.route_app_labels
        ):
           return True
        
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth and contenttypes apps only appear in the
        'default' database.
        """
        if app_label in self.route_app_labels:
            return db == 'default'
        return None


    # def allow_syncdb(self, db, model):
    #     """Make sure that apps only appear in the related database."""
    #     if db in settings.DATABASE_APPS_MAPPING.values():
    #         return settings.DATABASE_APPS_MAPPING.get(model._meta.app_label) == db
    #     elif settings.DATABASE_APPS_MAPPING.has_key(model._meta.app_label):
    #         return False
    #     return None
