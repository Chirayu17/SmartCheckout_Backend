class ImageDBRouter:
  

    def db_for_read(self, model, **hints):
        """
        Specify the database to use for read operations on Image models.
        """
        if model._meta.app_label == 'images':
            return 'mongo'
        return 'default'

    def db_for_write(self, model, **hints):
        """
        Specify the database to use for write operations on Image models.
        """
        if model._meta.app_label == 'images':
            return 'mongo'
        return 'default'
    
    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'images' or obj2._meta.app_label == 'images':
            # Allow relations between objects in the 'images' app
            return True
        
        # Allow relations involving the ContentType model
        if obj1._meta.model_name == 'contenttype' or obj2._meta.model_name == 'contenttype':
            return True
        
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Allow migrations for the Image app's models on the 'image_db' database.
        """
        if app_label == 'images':
            return db == 'mongo'
        return 'default'
