from rest_framework import permissions
from apps.project.models import *

class CommentIsAuthorOrReadonly(permissions.BasePermission):
    
    def has_permission(self, request, view):
        # �������������� ��û�� ���ö� �׳� ����Ʈ Ȯ���� �� �ְ�
        if request.data.get('client') ==  None:
            return True
        commentClient = request.data.get('client')
        commentClient = Client.objects.get(id = commentClient).user.id
        commentProject = request.data.get('project')
        commentProject = Project.objects.get(id = commentProject).client.user.id
        # ��û�� ���� ������ Ŀ��Ʈ�� �ۼ��� �����̰� Ŀ��Ʈ�� ���� ������Ʈ�� �ۼ��� �����̸� ������ �ش�.
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
        # �������������� ��û�� ���ö� �׳� ����Ʈ Ȯ���� �� �ְ�
        if request.data.get('client') ==  None:
            return False
        requestProject = request.data.get('project')
        requestProject = Project.objects.get(id = requestProject)
        # ��û�� ���� ������ ���並 �ۼ��� �����̰� ���䰡 ���� ������Ʈ�� �ۼ��� �����̸� ������ �ش�.
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
        # �������������� ��û�� ���ö� �׳� ����Ʈ Ȯ���� �� �ְ�
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
