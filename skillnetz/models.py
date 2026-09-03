from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    ROLE_CHOICES = ( 
    ("freelancer", "Freelancer"), 
    ("client", "Client"),
    ("admin","Admin"))
    role = models.CharField(max_length=20,choices=ROLE_CHOICES,default="admin")
    linkedin_id = models.CharField(null=True,blank=True,max_length=20)
    paypal_id = models.CharField(null=True,blank=True,max_length=50)
    dp_img = models.ImageField(upload_to="img",blank=True,null=True,default="img/dp.jpg")
    skill = models.ManyToManyField("Skills",blank=True)
    def __str__(self): 
        return self.username


class Job(models.Model):
    job_title = models.CharField(max_length=50)
    skill = models.ManyToManyField("Skills")
    price = models.CharField(max_length=50)
    description = models.TextField()
    post_date = models.DateField(null=True,blank=True,auto_now_add=True)
    job_image = models.ImageField(upload_to="job_images/",null=True,blank=True)
    post_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE)

class ActiveJob(models.Model):
    job_title = models.CharField(max_length=50)
    skill = models.ManyToManyField("Skills")
    price = models.CharField(max_length=50)
    description = models.TextField()
    post_date = models.DateField(null=True,blank=True,auto_now_add=True)
    job_image = models.ImageField(upload_to="job_images/",null=True,blank=True)
    post_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    assign_to =models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='assign',null=True,blank=True)

class Skills(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self): 
        return self.name
    
class JobApplication(models.Model):
    applicant = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='send')
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='Pending')  # Pending, Accepted, Rejected
    is_accepted = models.BooleanField(default=False)
    reciver = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True, blank=True)

class Message(models.Model):
    sender =  models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name="s")
    reciver = models.ManyToManyField("CustomUser")
    msg = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    job = models.ForeignKey(ActiveJob, on_delete=models.CASCADE, related_name='messages',default=1)

class PaymentApplication(models.Model):
    job = models.ForeignKey(ActiveJob, on_delete=models.CASCADE)
    total_payment = models.DecimalField(max_digits=10, decimal_places=2,default=1)
    is_accepted = models.BooleanField(default=False)

class Payment(models.Model):
    job = models.ForeignKey(ActiveJob, on_delete=models.CASCADE,default=1)
    name = models.CharField(max_length=100,null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_id = models.CharField(max_length=255)  # Add this line to include payment_id
    successful = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.amount}  - {self.payment_id}"

class Fileattachment(models.Model):
    job =models.ForeignKey(ActiveJob,on_delete=models.CASCADE)
    file = models.FileField(upload_to='attachment/')

class Work(models.Model):
    job =models.ForeignKey(ActiveJob,on_delete=models.CASCADE)
    work = models.CharField(max_length=3)

class SavedJob(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='saved_jobs')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='saved_by')
    saved_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')

class Feedback(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rating} star(s) - {self.user or 'Anonymous'}"