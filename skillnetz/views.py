from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db.models import Q
from . models import CustomUser,Job,Skills,JobApplication,ActiveJob,Message,PaymentApplication,Payment,Fileattachment,Work,SavedJob,Feedback
from .utils import send_email_to,send_application_mail
from django.contrib.auth import logout as logouts
import razorpay
from django.views.decorators.csrf import csrf_exempt
import http.client
import json
import base64
# Create your views here.



def signupclient(request):

    if request.user.is_authenticated:
        return redirect('home')
    
    else:
        if request.method=="POST":
            
            request.session['first_name']= request.POST['first_name']
            request.session['last_name'] = request.POST['last_name']
            request.session['linkedin_id']= request.POST['linkedin_id']
            email = request.POST['email']
            request.session['email'] = email
            request.session['password1'] = request.POST['password1']
            otp = send_email_to(email)
            request.session['otp']= otp
            
            return redirect('otp')
    
    return render(request,"signupclient.html")


def signup(request):

    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method=="POST":

            skill_string = request.POST.get('skill')
            request.session['role'] = request.POST.get('choice')
            skill_array = skill_string.split(',')
            request.session['list']= skill_array
            return redirect('signupclient')
                            
    return render(request,"signup.html")


def login(request):

    if request.user.is_authenticated:
        return redirect('home')
    
    else:
        if request.method=="POST":
            
            username = request.POST['username']
            password= request.POST['password']
            user = auth.authenticate(username=username, password=password)
            
            if user is not None:
                auth.login(request,user)
                return redirect('home')
            else:
                error="Invalid credentials. Please try again."
                return render(request,'login.html',{'error':error})
        
    return render(request,'login.html')

def logout(request):
    if request.method=='POST':
        logouts(request)
        return redirect('login')

def otp(request):

    if request.user.is_authenticated:
        return redirect('home')
    
    else:
        first_name=request.session['first_name']
        last_name=request.session['last_name']
        linkedin_id=request.session['linkedin_id']
        email=request.session['email']
        role =request.session['role']
        password1=request.session['password1']
        otp= request.session['otp']
        skill_array = request.session['list']

        if request.method=="POST":
            digit1= request.POST['digit1']
            digit2= request.POST['digit2']
            digit3= request.POST['digit3']
            digit4= request.POST['digit4']
            userotp =int(digit1+digit2+digit3+digit4)

            if otp==userotp:
                data= CustomUser.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=email,password=password1,linkedin_id=linkedin_id,role=role)
                for i in skill_array:
                    existing_skill = Skills.objects.filter(name=i).first()
                    if existing_skill:
                        # Author already exists, associate the existing author with the new book
                        data.skill.add(existing_skill)

                return redirect('login')
            
            else:
                error="Invalid OTP . Please try again"
                return render(request,"otp.html",{"error":error})
    return render(request,"otp.html")


def home(request):
    user = request.user
    return render(request,"home.html",{'user':user})

def findtalent(request):

    if request.method=="POST":

        job_title= request.POST['job-title']
        price= request.POST['budget']
        description= request.POST['description']
        job_image = request.FILES.get('image')
        post_by =request.user

        skill_string = request.POST.get('skill')
        skill_array = skill_string.split(',')
        job = Job.objects.create(job_title=job_title,price=price,description=description,job_image=job_image,post_by=post_by)
        for i in skill_array:
            existing_skill = Skills.objects.filter(name=i).first()
            if existing_skill:
                # Author already exists, associate the existing author with the new book
                job.skill.add(existing_skill)
        
    return render(request,'findtalent.html')

def findwork(request):

    skills = Skills.objects.all()
    query = request.GET.get('q', '').strip()
    jobs = Job.objects.all()

    if query:
        jobs = jobs.filter(
            Q(job_title__icontains=query) |
            Q(description__icontains=query) |
            Q(skill__name__icontains=query)
        ).distinct()

    jobs_with_skill = {}
    for i in skills:
        specific_skill_name = i.name
        jobs_with_skill[specific_skill_name] = jobs.filter(skill__name=specific_skill_name)

    filtered_data = {key: value for key, value in jobs_with_skill.items() if value}

    saved_job_ids = []
    if request.user.is_authenticated:
        saved_job_ids = list(SavedJob.objects.filter(user=request.user).values_list('job_id', flat=True))

    data={
        'skills':skills,
        'jobs':jobs,
        'query':query,
        'jobs_with_skill': filtered_data,
        'saved_job_ids': saved_job_ids,
    }
    return render(request,'findwork.html',data)

def job_details(request, job_id):

    job =get_object_or_404(Job,pk=job_id)
    user = request.user
    reciver = job.post_by  # Set the reciver to the user who posted the job
    has_applied = JobApplication.objects.filter(job=job,applicant=user).exists() if user.is_authenticated else False
    is_saved = SavedJob.objects.filter(job=job, user=user).exists() if user.is_authenticated else False
    applicant_count = JobApplication.objects.filter(job=job).count()

    if request.method=="POST":
        if not user.is_authenticated:
            return redirect('login')
        applicant= user
        apply_job = JobApplication(applicant=applicant,job=job,reciver=reciver)
        apply_job.save()
        has_applied =True

    return render(request,'job_detail.html',{'job':job,'has_applied': has_applied,'is_saved': is_saved,'applicant_count': applicant_count})

def job_applications(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    applications = JobApplication.objects.filter(job=job)
    return render(request, 'job_applications.html', {'job': job, 'applications': applications})

def activejobs(request):
    user_posts = ActiveJob.objects.filter(post_by=request.user)
    return render(request, 'activejobs.html', {'user_posts': user_posts})

def accept_application(request,job_id, application_id):
    job = get_object_or_404(Job, id=job_id)
    application = get_object_or_404(JobApplication, id=application_id)
    # Mark the application as accepted (you may have a field for this in your Application model)
    application.is_accepted = True
    application.save()

    # Delete all other applications related to this job
    other_applications = JobApplication.objects.filter(job=job).exclude(id=application.id).delete()

    # Create a new ActiveJob using the data from the existing Job
    active_job = ActiveJob.objects.create(
        job_title=job.job_title,
        price=job.price,
        description=job.description,
        post_date=job.post_date,
        job_image=job.job_image,
        post_by=job.post_by,
        assign_to=application.applicant,
    )
    active_job.skill.set(job.skill.all())

    applicant_email = application.applicant.email
    applicant_username = application.applicant.username

    # Send an email to the user
    send_application_mail(applicant_email, job.job_title, applicant_username)
    # Delete the job from the Job model
    job.delete()
    return redirect('activejobs')

def handling_404(request, exception):
    return render(request,'404.html', status=404)

def about(request):
    return render(request,"about.html")

def user_jobs(request):
    user_posts = Job.objects.filter(post_by=request.user)
    return render(request, 'myjobs.html', {'user_posts': user_posts})

def user_work(request):
    applied_jobs = JobApplication.objects.filter(applicant=request.user)
    return render(request, 'mywork.html', {'applied_jobs': applied_jobs})

def workingjobs(request):
    working_jobs = ActiveJob.objects.filter(assign_to=request.user)
    return render(request, 'workingjobs.html', {'working_jobs': working_jobs})

def dashboard(request,job_id):

    job = get_object_or_404(ActiveJob, pk=job_id)

    if request.user==job.assign_to:

        has_applied = PaymentApplication.objects.filter(job=job)
        payment_done = Payment.objects.filter(job=job)
        chat = Message.objects.filter(job=job).order_by('timestamp')
        my_file = Fileattachment.objects.filter(job=job)

        if has_applied:
            for payment in has_applied:
                value=payment.is_accepted
        else:
            value= False
        
        if payment_done:
            for pay in payment_done:
                value1=pay.successful
        else:
            value1= False

        return render(request,"freelancerdashborad.html",{'data': job,'messages': chat,'has_applied':has_applied,'payment_done':payment_done,'my_file': my_file,'value':value,'value1':value1})
    
    elif request.user==job.post_by:

        request_payemnt = PaymentApplication.objects.filter(job=job)
        payment_done = Payment.objects.filter(job=job)
        chat = Message.objects.filter(job=job).order_by('timestamp')
        my_file = Fileattachment.objects.filter(job=job)
        works = Work.objects.filter(job=job)
        if works:
            for work in works:
                work_value=work.work
        else:
            work_value="0"
        
        paisa_price=int(job.price)*100
        if request.method == "POST":
            amount = job.price
            client = razorpay.Client(
                auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            
            payment = client.order.create({'amount': amount*100, 'currency': 'INR',
                                       'payment_capture': '1'})
    
        return render(request,"clientdashborad.html",{'data': job,'messages': chat,'payment_done':payment_done,'request_payemnt':request_payemnt,'my_file': my_file,'work_value':work_value,'paisa_price':paisa_price})

    else:
        return HttpResponse("You are not an client or an freelancer of this active job")

def chat_submit(request,job_id):
    job = get_object_or_404(ActiveJob, pk=job_id)
    
    freelancer= job.assign_to
    client = job.post_by
    
    if request.method=="POST":
        msg= request.POST['msg']
        sender=request.user
        message = Message.objects.create(msg=msg,sender=sender,job=job)
        message.reciver.add(freelancer)
        message.reciver.add(client)
        message.save()
    return redirect('dashboard',job_id=job_id)

def paymentapp_submit(request,job_id):
    job = get_object_or_404(ActiveJob, pk=job_id)

    if request.method=="POST":
        application = PaymentApplication.objects.create(job=job,total_payment=job.price)
        application.save()
    return redirect('dashboard',job_id=job_id)

def collect_money(request,job_id):
    user =request.user
    job = get_object_or_404(ActiveJob, pk=job_id)

    if request.method=="POST":

        name = request.POST['name']
        contactno = request.POST['contactno']
        ifsccode = request.POST['ifsccode']
        accountno = request.POST['accountno']


        #create contact
        auth_header = 'Basic ' + base64.b64encode(
            f"{settings.RAZORPAY_KEY_ID}:{settings.RAZORPAY_KEY_SECRET}".encode()
        ).decode()
        conn = http.client.HTTPSConnection("api.razorpay.com")
        payload = json.dumps({
        "name": name,
        "email": user.email,
        "contact": contactno,
        "type": "employee",
        "reference_id": "Acme Contact ID 12345",
        "notes": {
            "random_key_1": "Make it so.",
            "random_key_2": "Tea. Earl Grey. Hot."
        }
        })
        headers = {
        'Content-Type': 'application/json',
        'Authorization': auth_header
        }
        conn.request("POST", "/v1/contacts", payload, headers)
        res = conn.getresponse()
        data = res.read()
        decoded_data= data.decode("utf-8")
        decoded_dict = json.loads(decoded_data)
        id=decoded_dict.get('id')


        #create fund acc to each contact
        con = http.client.HTTPSConnection("api.razorpay.com")
        payload = json.dumps({
        "contact_id": id,
        "account_type": "bank_account",
        "bank_account": {
            "name": name,
            "ifsc": ifsccode,
            "account_number": accountno
        }
        })
        headers = {
        'Content-Type': 'application/json',
        'Authorization': auth_header
        }
        con.request("POST", "/v1/fund_accounts", payload, headers)
        res = con.getresponse()
        data = res.read()
        decoded_data= data.decode("utf-8")
        decoded_dict = json.loads(decoded_data)
        f_id=decoded_dict.get('id')
        amount=(int(job.price)*100)


        #create payout for an user
        conn3 = http.client.HTTPSConnection("api.razorpay.com")
        payload = json.dumps({
        "account_number": "2323230097738720",
        "fund_account_id": f_id,
        "amount": amount,
        "currency": "INR",
        "mode": "NEFT",
        "purpose": "payout",
        "queue_if_low_balance": True,
        "reference_id": "Acme Transaction ID 12345",
        "narration": "Acme Corp Fund Transfer",
        "notes": {
            "random_key_1": "Make it so.",
            "random_key_2": "Tea. Earl Grey. Hot."
        }
        })
        headers = {
        'Content-Type': 'application/json',
        'Authorization': auth_header
        }
        conn3.request("POST", "/v1/payouts", payload, headers)
        res = conn3.getresponse()
        data = res.read()

        existing_payment = Payment.objects.filter(job=job).first()
        
        if existing_payment:
            # Update the existing instance
            existing_payment.successful = True
            existing_payment.save()

        return render(request,"collectsucess.html")
    
    return render(request,'collect.html')

def file_submit(request,job_id):
    job = get_object_or_404(ActiveJob, pk=job_id)

    if request.method=="POST":
        file = request.FILES.get('file')
        file_obj = Fileattachment.objects.create(job=job,file=file)
        file_obj.save()

    return redirect('dashboard',job_id=job_id)

def work_submit(request, job_id):
    job = get_object_or_404(ActiveJob, pk=job_id)

    if request.method == "POST":
        work_text = request.POST['work']
        
        # Check if a Work instance already exists for the given job
        existing_work = Work.objects.filter(job=job).first()
        
        if existing_work:
            # Update the existing instance
            existing_work.work = work_text
            existing_work.save()
        else:
            # Create a new instance
            new_work = Work.objects.create(job=job, work=work_text)
            new_work.save()
        
    return redirect('dashboard', job_id=job_id)


@csrf_exempt
def success(request,job_id):
    job = get_object_or_404(ActiveJob, pk=job_id)
    user = job.post_by.first_name
    application = get_object_or_404(PaymentApplication, job=job)

    if request.method == "POST":
        amount = job.price
        payment_id = request.POST.get('razorpay_payment_id')
        # Create a Payment instance
        payment = Payment.objects.create(job=job,amount=amount, payment_id=payment_id,name=user)
        application.is_accepted=True
        application.save()
        return render(request, 'success.html', {'payment_instance': payment})

    # Handle GET requests if needed
    return render(request, 'success.html')


@login_required
def save_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    saved = SavedJob.objects.filter(job=job, user=request.user).first()

    if saved:
        saved.delete()
    else:
        SavedJob.objects.create(job=job, user=request.user)

    return redirect(request.META.get('HTTP_REFERER', 'findwork'))


@login_required
def saved_jobs(request):
    saved = SavedJob.objects.filter(user=request.user).select_related('job').order_by('-saved_on')
    return render(request, 'savedjobs.html', {'saved_jobs': saved})


def feedback_submit(request):
    if request.method == "POST":
        rating = request.POST.get('rating', '')
        comment = request.POST.get('comment', '')

        if rating.isdigit() and 1 <= int(rating) <= 5:
            Feedback.objects.create(
                user=request.user if request.user.is_authenticated else None,
                rating=int(rating),
                comment=comment,
            )

    return redirect(request.META.get('HTTP_REFERER', 'home'))

