from django import forms

from kitchenrock_api.models.food_recipe import FoodMaterial
from kitchenrock_api.models.materials import MaterialNutrition
from kitchenrock_api.models.user import User


class PasswordUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PasswordUserForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Since the pk is set this is not a new instance
            self.fields['password'].widget = forms.HiddenInput()

    def clean_password(self):
        if self.instance and self.instance.pk:
            return self.instance.password
        else:
            return self.cleaned_data['password']


class MaterialNutritionForm(forms.ModelForm):
    value = forms.FloatField(min_value=0)
    class Meta:
        model = MaterialNutrition
        fields = '__all__'

class FoodMaterialForm(forms.ModelForm):
    value = forms.FloatField(label="Value", min_value=0)
    class Meta:
        model = FoodMaterial
        fields = '__all__'