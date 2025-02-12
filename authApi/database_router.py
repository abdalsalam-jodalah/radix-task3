class MyDatabaseRouter:
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        blocked_apps = {"auth", "admin", "contenttypes", "sessions", "messages"}
        return app_label not in blocked_apps
