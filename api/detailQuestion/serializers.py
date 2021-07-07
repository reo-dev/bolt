from rest_framework import serializers

from apps.detailQuestion.models import *

class DetailQuestionTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailQuestionTitle
        fields = ['id', 'question', 'createdAt']
        
class DetailQuestionSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailQuestionSelect
        fields = ['id', 'title', 'nextTitle', 'select', 'createdAt']

class DetailQuestionSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailQuestionSave
        fields = ['id', 'request', 'question', 'select', 'createdAt']

    def createFromList (self, dataList):
        for data in dataList:
            self.create(data)