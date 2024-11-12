# forms.py
from django import forms
from .models import Prescription, Medicine,Customer

class PrescriptionForm(forms.ModelForm):
    medicines = forms.ModelMultipleChoiceField(
        queryset=Medicine.objects.all(),  # Fetch all medicines from the database
        widget=forms.CheckboxSelectMultiple(),  # Display medicines as checkboxes
        required=True  # Make this field required
    )

    class Meta:
        model = Prescription
        fields = ['doctor_name', 'medicines']

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'contact_info', 'address'] 
