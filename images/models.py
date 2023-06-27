from django.db import models
from django.utils import timezone
from gridfs import GridFS
from gridfs_storage.storage import GridFSStorage
# Create a GridFS storage instance
# gridfs_storage = GridFSStorage(collection='product_images')

class Images(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    image = models.BinaryField()


  

    class Meta:
        app_label = 'images'
        db_table = 'product_images'
