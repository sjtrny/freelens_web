from django.forms import ModelForm

from .models import Tag


class TagForm(ModelForm):
    class Meta:
        model = Tag
        # fields = '__all__'  # Automatically include all fields
        fields = ["_data"]

        labels = {
            "_data": "Message (e.g. URL)",  # Change the field name on the form
        }
