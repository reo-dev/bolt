from rest_framework import permissions
from apps.project.models import *

class CommentIsAuthorOrReadonly(permissions.BasePermission):
    
    def has_permission(self, request, view):
        # 어드민페이지에서 요청이 들어올땐 그냥 리스트 확인할 수 있게
        if request.data.get('client') ==  None:
            return True
        commentClient = request.data.get('client')
        commentClient = Client.objects.get(id = commentClient).user.id
        commentProject = request.data.get('project')
        commentProject = Project.objects.get(id = commentProject).client.user.id
        # 요청을 날린 유저가 커멘트를 작성한 유저이고 커멘트가 속한 프로젝트를 작성한 유저이면 권한을 준다.
        if request.user.id == commentClient and  commentClient == commentProject:
            return request.user.is_authenticated
        else:
            return False
    
    def has_object_permission(self, request, views, obj):
        projectClient = Client.objects.get(id = request.data['client']).user

        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.project.client.user == request.user and request.user == projectClient


class ReveiwIsAuthorOrReadonly(permissions.BasePermission):
    
    def has_permission(self, request, view):
        # 어드민페이지에서 요청이 들어올땐 그냥 리스트 확인할 수 있게
        if request.data.get('client') ==  None:
            return False
        requestProject = request.data.get('project')
        requestProject = Project.objects.get(id = requestProject)
        # 요청을 날린 유저가 리뷰를 작성한 유저이고 리뷰가 속한 프로젝트를 작성한 유저이면 권한을 준다.
        if request.user.id == requestProject.client.user.id:
            return request.user.is_authenticated
        else:
            return False
    
    def has_object_permission(self, request, views, obj):

        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.project.client.user == request.user

class ProjectIsAuthorOrReadonly(permissions.BasePermission):
    
    def has_permission(self, request, view):
        # 어드민페이지에서 요청이 들어올땐 그냥 리스트 확인할 수 있게
        if request.data.get('client') ==  None:
            return False
        client = Client.objects.get(id = request.data['clientId']).user.id
        
        if request.user.id == client:
            return request.user.is_authenticated
        else:
            return False
    
    def has_object_permission(self, request, views, obj):
        
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.client.user == request.user
