from django.db import models

# Create your models here.
class userRegister(models.Model):
    username=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    password=models.CharField(max_length=100)
    user_image=models.ImageField(upload_to='images/')

    def __str__(self):
        return self.username

class todo(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField()
    is_completed=models.BooleanField(default=False)
    is_deleted=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    user=models.ForeignKey(userRegister,on_delete=models.CASCADE)

    def __str__(self):
        return self.title

