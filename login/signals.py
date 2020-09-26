from django.dispatch import receiver,Signal
notificaton = Signal(providing_args=['request','Profile'])

@receiver(notificaton)
def online_active(sender,**kwargs):
    print("------------------------------")
    print("sender : " , sender )
    print(kwargs)
    print("------------------------------")


# from django.db.models.signals import post_save
# from Home.models import Post,Profile,FriendRequest,PostComment
# from django.dispatch import receiver
# from Home.models import Profile


# #
# @receiver(sender = Profile)
# def online(sender,request,user,**kwargs):
#     print("-----------------")


# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
# 	if created:
# 		Profile.objects.create(user=instance)
#
#
# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
# 	print('fsdf',sender)
# 	print('instance',instance)
# 	print('created',created)
# 	if created:
# 		Profile.objects.create(user=instance)
#
#
# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwargs):
# 		instance.profile.save(),