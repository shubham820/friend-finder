from django.db import models
from django.utils.timezone import now
from django.db.models import (Model, TextField, DateTimeField, ForeignKey,
                               CASCADE)
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer                               

# Create your models here.

class Profile(models.Model):
    profile_id = models.AutoField(primary_key = True )
    fname = models.CharField(max_length= 50,null=False)
    lname = models.CharField(max_length= 50, null=False)
    email = models.CharField(max_length=50,null= False)
    password = models.CharField(max_length=100 ,null=False)
    city = models.CharField(max_length=50,null=False)
    birthdate = models.CharField(max_length=100,null=False)
    is_active = models.BooleanField(default = "")
    profile_image=models.ImageField(upload_to='profile/img',default='')
    friends = models.ManyToManyField("Profile", blank=True)

    def __str__(self):
        return self.fname

class Post(models.Model):
    sno = models.AutoField(primary_key=True)
    id_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    pub_date = models.DateField(default = now)
    post_img = models.ImageField(upload_to="profile/img",default="",null = True,blank=True )
    post_video = models.FileField(upload_to="profile/video",default="",null=True,blank=True)
    status = models.TextField(default="")
    likes = models.ManyToManyField(Profile,related_name="Post_like",blank=True )

    def __str__(self):
        return str(self.id_profile)
class FriendRequest(models.Model):
    to_user = models.ForeignKey('Profile', related_name='to_user', on_delete=models.CASCADE)
    from_user = models.ForeignKey('Profile', related_name='from_user', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return (f"{self.from_user}-->{self.to_user}")

class PostComment(models.Model):
    sno = models.AutoField(primary_key=True)
    comment_id = models.IntegerField(default=1)
    comment = models.TextField()
    user = models.ForeignKey(Profile,on_delete =models.CASCADE)
    reply_of_comnt = models.ForeignKey('self',on_delete=models.CASCADE,null=True) 
    post = models.ForeignKey(Post, on_delete=models.CASCADE ,null=False)
    timestamp = models.DateTimeField(default = now)
    likes = models.ManyToManyField(Profile,related_name="comment_like",blank=True )
    
    def __str__(self):
        return f"{self.post}get comment by{self.user}"




class MessageModel(models.Model):
    """
    This class represents a chat message. It has a owner (user), timestamp and
    the message body.

    """
    user = ForeignKey(Profile, on_delete=CASCADE, verbose_name='user',
                      related_name='from_user', db_index=True)
    recipient = ForeignKey(Profile, on_delete=CASCADE, verbose_name='recipient',
                           related_name='to_user', db_index=True)
    timestamp = DateTimeField('timestamp', auto_now_add=True, editable=False,
                              db_index=True)
    body = TextField('body')

    def __str__(self):
        return str(self.id)

    def characters(self):
        """
        Toy function to count body characters.
        :return: body's char number
        """
        return len(self.body)

    def notify_ws_clients(self):
        """
        Inform client there is a new message.
        """
        notification = {
            'type': 'recieve_group_message',
            'message': '{}'.format(self.id)
        }

        channel_layer = get_channel_layer()
        print("user.id {}".format(self.user.id))
        print("user.id {}".format(self.recipient.id))

        async_to_sync(channel_layer.group_send)("{}".format(self.user.id), notification)
        async_to_sync(channel_layer.group_send)("{}".format(self.recipient.id), notification)

    def save(self, *args, **kwargs):
        """
        Trims white spaces, saves the message and notifies the recipient via WS
        if the message is new.
        """
        new = self.id
        self.body = self.body.strip()  # Trimming whitespaces from the body
        super(MessageModel, self).save(*args, **kwargs)
        if new is None:
            self.notify_ws_clients()

    # Meta
    class Meta:
        app_label = 'core'
        verbose_name = 'message'
        verbose_name_plural = 'messages'
        ordering = ('-timestamp',)






# class MessageModel(Model):
#     """
#     This class represents a chat message. It has a owner (user), timestamp and
#     the message body.

#     """
#     user = ForeignKey(User, on_delete=CASCADE, verbose_name='user',
#                       related_name='from_user', db_index=True)
#     recipient = ForeignKey(User, on_delete=CASCADE, verbose_name='recipient',
#                            related_name='to_user', db_index=True)
#     timestamp = DateTimeField('timestamp', auto_now_add=True, editable=False,
#                               db_index=True)
#     body = TextField('body')

#     def __str__(self):
#         return str(self.id)

#     def characters(self):
#         """
#         Toy function to count body characters.
#         :return: body's char number
#         """
#         return len(self.body)

#     def notify_ws_clients(self):
#         """
#         Inform client there is a new message.
#         """
#         notification = {
#             'type': 'recieve_group_message',
#             'message': '{}'.format(self.id)
#         }

#         channel_layer = get_channel_layer()
#         print("user.id {}".format(self.user.id))
#         print("user.id {}".format(self.recipient.id))

#         async_to_sync(channel_layer.group_send)("{}".format(self.user.id), notification)
#         async_to_sync(channel_layer.group_send)("{}".format(self.recipient.id), notification)

#     def save(self, *args, **kwargs):
#         """
#         Trims white spaces, saves the message and notifies the recipient via WS
#         if the message is new.
#         """
#         new = self.id
#         self.body = self.body.strip()  # Trimming whitespaces from the body
#         super(MessageModel, self).save(*args, **kwargs)
#         if new is None:
#             self.notify_ws_clients()

#     # Meta
#     class Meta:
#         app_label = 'core'
#         verbose_name = 'message'
#         verbose_name_plural = 'messages'
#         ordering = ('-timestamp',)
