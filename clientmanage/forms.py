from django import forms
from .models import Client



class ClientForm(forms.ModelForm):
    delete = forms.BooleanField(required=False, label="Delete Client", widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    
    class Meta:
        model = Client
        fields = [
            'companyName', 'divisionName', 'titleName', 'sirName', 
            'givenName', 'postCode', 'address1', 'address2', 
            'tel', 'cell', 'email', 'email2', 'note', 'eng'
        ]
        widgets = {
            'companyName': forms.TextInput(attrs={
                'class': 'form-control',  # Bootstrap styling
                'style': 'width: 100%; max-width: 700px;',  # Custom width
                'placeholder': 'Enter company name'
            }),
            'divisionName': forms.TextInput(attrs={
                'class': 'form-control',  # Bootstrap styling
                'style': 'width: 100%; max-width: 700px;',  # Custom width
                'placeholder': 'Enter company name'
            }),
            'address1': forms.TextInput(attrs={
                'class': 'form-control',  # Bootstrap styling
                'style': 'width: 100%; max-width: 700px;',  # Custom width
                'placeholder': 'Enter company name'
            }),
            'address2': forms.TextInput(attrs={
                'class': 'form-control',  # Bootstrap styling
                'style': 'width: 100%; max-width: 700px;',  # Custom width
                'placeholder': 'Enter company name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'style': 'width: 100%; max-width: 700px;',
                'placeholder': 'Enter email'
            }),
            'email2': forms.EmailInput(attrs={
                'class': 'form-control',
                'style': 'width: 100%; max-width: 700px;',
                'placeholder': 'Enter email'
            }),
            'note': forms.Textarea(attrs={  # Use Textarea widget here
                'class': 'form-control',
                'style': 'width: 100%; max-width: 700px; height: 150px;',  # Set height for textarea
                'placeholder': 'Enter additional notes here...'
            }),
            # Add similar widgets for other fields as needed
        }


class CsvUploadForm(forms.Form):
    csv_file = forms.FileField()