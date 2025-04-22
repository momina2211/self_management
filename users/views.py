from rest_framework import  generics
from django.contrib.auth import get_user_model
from users.serializers import UserSignupSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
User = get_user_model()


class SignUpView(generics.ListCreateAPIView):
    serializer_class = UserSignupSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token,created = Token.objects.get_or_create(user=user)
        response_data={
            'token': token.key,
            'user':serializer.data
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        users = User.objects.all()
        serializer = UserSignupSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LoginView(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        User = get_user_model()
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                token = Token.objects.get(user=user)

                response_data = {
                    'token': token.key,
                    'user': {
                        'id': user.id,
                        'email': user.email,
                    }
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)

        except User.DoesNotExist:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)