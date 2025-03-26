class MyDatabaseRouter:
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        blocked_apps = {"auth", "admin", "contenttypes", "sessions", "messages"}
        print(f"Checking migration for: {app_label}") 

        return app_label not in blocked_apps
