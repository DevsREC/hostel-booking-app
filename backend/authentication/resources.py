from import_export import resources
from .models import User

class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'phone_number', 'year', 'roll_no', 'dept', 'gender']