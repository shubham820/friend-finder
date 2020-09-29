from django.contrib import admin
from .models import Profile,Post,FriendRequest,PostComment,MessageModel
# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [id,'fname','lname','email']


@admin.register(Post)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [id,"id_profile","pub_date","status"]

@admin.register(FriendRequest)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [id,"from_user","to_user"]

@admin.register(PostComment)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [id,"sno","post","user","comment_id"]

@admin.register(MessageModel)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [id,"user","recipient","timestamp"]


# admin.site.register(Profile,ProfileAdmin)