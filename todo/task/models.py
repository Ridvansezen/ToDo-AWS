from django.db import models

class TodoTaskModel(models.Model):
    title = models.CharField(max_length=70, blank=False, null=False, unique=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
