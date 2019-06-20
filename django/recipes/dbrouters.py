class AuthRouter:
    """
    A router to control all database operations on models in the
    auth application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read recipes models go to auth_db.
        """
        if model._meta.app_label == 'recipes':
            return 'auth_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write recipes models go to auth_db.
        """
        if model._meta.app_label == 'recipes':
            return 'auth_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the recipes app is involved.
        """
        if obj1._meta.app_label == 'recipes' or \
           obj2._meta.app_label == 'recipes':
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the recipes app only appears in the 'auth_db'
        database.
        """
        if app_label == 'recipes':
            return db == 'auth_db'
        return None