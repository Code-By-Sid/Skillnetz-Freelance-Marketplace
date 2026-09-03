import random
from django.core.mail import send_mail
from django.conf import settings
def generate_random_number(min_value,max_value):
    return random.randint(min_value,max_value)

def send_email_to(email):
    otp = generate_random_number(1000,9999)
    subject = " OTP VERIFICATION"
    message = f"Your OTP for verification is:{otp}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject,message,from_email,recipient_list,fail_silently=False)
    return otp

def send_application_mail(email,title,username):
    subject = f"{title} Your Job Application has been Accepted!"
    message = f"Dear {username},\n\nCongratulations! Your job application for the job {title} has been accepted. \nStart Working on your job here "" \nThank you for your interest.\n\nBest regards,\nThe Job Portal Team"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject,message,from_email,recipient_list,fail_silently=False)