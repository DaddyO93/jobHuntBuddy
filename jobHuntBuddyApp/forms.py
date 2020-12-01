from django import forms
from django.forms import fields
from .models import Position


class PositionForm (forms.ModelForm):
    class Meta:
        model = Position
        fields = [
            'date_applied',
            'position',
            'company',
            'note',
        ]