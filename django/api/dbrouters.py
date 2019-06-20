class FoodDatabaseRouter(object):
    
    """
    How to route database calls for the api.food's models (in this case, for an app named Example).
    All other models will be routed to the default router in the DATABASE_ROUTERS setting if applicable.
    """

    def db_for_read(self, model, **hints):
        """Send all read operations on API app models to 'food' db."""
        if model._meta.app_label == 'api':
            return 'food'
        return None

    def db_for_write(self, model, **hints):
        """Send all write operations on API app models to no db."""
        if model._meta.app_label == 'api':
            return False
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Ensure that the api app's models get created on the right database."""
        if app_label == 'api':
            # Ensure api app is not migrated on the food (recipes_db) database.
            return False
        elif db == 'food':
            # Also ensure that all other apps don't get migrated on the food (recipes_db) database.
            return False

        # No opinion for all other scenarios
        return None