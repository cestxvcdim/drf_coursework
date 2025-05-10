from rest_framework.generics import CreateAPIView

from users.models import User
from users.serializers import UsersSerializer


class UserRegisterView(CreateAPIView):
    serializer_class = UsersSerializer
    queryset = User.objects.all()
