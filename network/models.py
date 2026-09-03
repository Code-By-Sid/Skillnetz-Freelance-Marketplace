from django.db import models
from skillnetz.models import CustomUser
from django.db.models.signals import post_save
from django.dispatch import receiver



class profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, related_name="pro")
    follows=models.ManyToManyField("self",related_name="followed_by",symmetrical=False,blank=True)
    skills=models.ManyToManyField("Skills")
    saved_profiles = models.ManyToManyField("self", related_name="saved_by", symmetrical=False, blank=True)


   
    def __str__(self):
        return self.user.username


class Skills(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self): 
        return self.name

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.pro.save()

class posts(models.Model):
    user=models.ForeignKey(CustomUser,related_name="posts",on_delete=models.CASCADE)
    body=models.CharField(max_length=200)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return(
             f"{self.user}"
             f"({self.created_at:%d-%m-%y})"
             f"{self.body}"
             )

class Resume(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,default=1)
    personal_info = models.TextField(default="none")
    experience=models.TextField(default="none")
    achievements = models.TextField(default="none")

class SavedProfile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='saved_profiles')
    saved_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='saved_by')

    class Meta:
        unique_together = ('user', 'saved_user')