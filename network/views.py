from skillnetz.models import CustomUser
from .models import profile,posts,Resume
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from .forms import PostForm
from django.db.models import Count

def get_profile_data(request,pk):
    if request.user.is_authenticated:
        try:
                Profile = profile.objects.get(user_id=pk)
            
                return Profile
        except profile.DoesNotExist:
                return None, None
    else:
        return redirect('login')
    

def profile_list(request):
    if request.user.is_authenticated:
        profiles = profile.objects.exclude(user=request.user).annotate(follower_count=Count('follows'))
        Profile = get_profile_data(request,request.user.pk)

        if request.method == "POST":
            saved_user_profile = request.user.pro
            action = request.POST.get('saving')  # Use get() to avoid MultiValueDictKeyError
            if action == "unsave":
                saved_user_profile.saved_profiles.remove(Profile)
            elif action == "saving":
                saved_user_profile.saved_profiles.add(Profile)
            saved_user_profile.save()  # Save the profile after adding or removing saved profiles

        return render(request, 'network.html', {"profiles": profiles, "Profile": Profile})
    else:
        return redirect('login')



def profiles(request,pk,page_type=None):
    if request.user.is_authenticated:
        user=request.user
        Profile=profile.objects.get(user_id=pk)
        Follows = Profile.follows.all()
        Posts = posts.objects.filter(user=Profile.user).order_by("-created_at")

        if page_type == 'followers':
            # Get the followers for the profile
            users_list = profile.objects.filter(follows=Profile)
            return render(request, "followers.html", {"users_list": users_list})

        elif page_type == 'following':
            # Get the profiles followed by the current profile
            follows_list = Profile.follows.all()
            return render(request, "following.html", {"follows_list": follows_list})
        
        if request.method=="POST":
            current_user_profile=request.user.pro
            action=request.POST['follow']
            if action=="unfollow":
                current_user_profile.follows.remove(Profile)
            elif action=="follow":
                current_user_profile.follows.add(Profile)

            current_user_profile.save()

    
        return render(request,"profile.html",{"Profile":Profile,"Follows": Follows,"Posts":Posts,"user":user})
    
    else:
        return redirect('login')



def user_post(request):
    if request.user.is_authenticated:
        Posts=posts.objects.all().order_by("-created_at")
        return render(request,'posts.html',{"Posts":Posts})
    else:
        return redirect('login')

def add_post(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('posts')  # Redirect to the success URL
    else:
        form = PostForm()
    return render(request, 'addpost.html', {'form': form})

def save_resume(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':

        personal_info = request.POST.get('profile_details')
        experience = request.POST.get('work_experience')
        achievements = request.POST.get('achievements')


        user = request.user


        if hasattr(user, 'resume'):

            resume = user.resume
            resume.personal_info = personal_info
            resume.experience = experience
            resume.achievements = achievements
            resume.save()
        else:

            resume = Resume(user=user, personal_info=personal_info, experience=experience, achievements=achievements)
            resume.save()

        return redirect('display_resume',user_id=user.id)
    else:
        resume = Resume.objects.filter(user=request.user).first()
        return render(request, 'edit_resume.html', {'resume': resume})
    
def display_resume(request, user_id):

    user = get_object_or_404(CustomUser, pk=user_id)


    resume = Resume.objects.filter(user=user).first()


    
    return render(request, 'resume.html', {'resume': resume, 'user': user})

def upload_img(request,user_id):

    if request.method == 'POST':

        dp = request.FILES.get('image')

        existing_user = CustomUser.objects.filter(id=user_id).first()
        
        if existing_user:
            # Update the existing instance
            existing_user.dp_img = dp
            existing_user.save()
        else:
            pass
    return redirect('profile',pk=user_id)
  