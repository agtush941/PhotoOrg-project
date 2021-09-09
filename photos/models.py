from django.db import models
from django.db.models.expressions import F
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    user = models.ForeignKey(User,on_delete = models.SET_NULL,null =True)
    name = models.CharField(max_length = 100,null = True,blank = True)
    
    def _str_(self):
        return self.name

class Photo(models.Model):
    desc = models.TextField()
    image = models.ImageField(null=False,blank = False)
    category = models.ForeignKey(Category,on_delete= models.SET_NULL,null = True,blank = True)
    
    def _str_(self):
        return self.desc
    def delete(self):
        self.image.delete(save=False)
        super().delete()