from django.contrib import admin
from django.contrib.auth.models import User,Group
from .models import profile,posts,Skills,Resume

admin.site.unregister(Group)


admin.site.register(profile)
admin.site.register(posts)
admin.site.register(Skills)
admin.site.register(Resume)


# Register your models here.
