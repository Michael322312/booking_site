from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ("phone",)
