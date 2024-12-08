from django import forms
from django.forms import modelformset_factory
from simple_kanban.models import Project, Swimlane

class SwimlaneForm(forms.ModelForm):
    class Meta:
        model = Swimlane
        fields = ['name', 'sort_order']
        widgets = {
          "name": forms.TextInput(attrs={
            "class": "form-control"
          }),
          "sort_order": forms.NumberInput(attrs={
            "class": "form-control", "min": 1
          })
        }

SwimlaneFormSet = modelformset_factory(Swimlane, form=SwimlaneForm, extra=0)