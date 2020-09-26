from django.apps import AppConfig


class LoginConfig(AppConfig):
    name = 'login'

    def ready(self):
        import login.signals




# <a href="/profile/post_like" class="btn text-green" name="post_like" value="{{i.id}}"><i class="icon ion-thumbsup"></i> 13</a>