from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from apps.account.models import User


class UpdateLastActivityMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response
        
    #def activity_view(self, request, view_func, view_args, view_kwargs):
        #print("1")
        #if request.user: #, 'The UpdateLastActivityMiddleware requires authentication middleware to be installed.'
          #if request.user.is_authenticated:
            #User.objects.filter(user__id=request.user).update(last_activity=timezone.now())
          #pass

    def __call__(self, request, *args, **kwargs):
        response = self.get_response(request)
        
        if request.user:
          if request.user.is_authenticated:
            User.objects.filter(id=request.user.id).update(last_activity=timezone.now())
            
        return response

    