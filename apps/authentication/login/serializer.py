from django.forms import ValidationError
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

UserModel = get_user_model()


class UserLoginSerializer(serializers.Serializer):
	registration = serializers.CharField()
	password = serializers.CharField()
	##
	def check_user(self, clean_data):
		user = authenticate(username=clean_data['registration'], password=clean_data['password'])
		if not user:
			raise ValidationError('user not found')
		return user
	

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserModel
		fields = ('registration',)
