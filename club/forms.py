from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string

import datetime

from .models import Member, Person


class MemberWithPersonForm(forms.Form):
    # Campos de Person
    names = forms.CharField(max_length=100, label="Nombres",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    surnames = forms.CharField(max_length=100, label="Apellidos",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    dni = forms.CharField(max_length=20, label="DNI",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(label="Email", required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    phone = forms.CharField(max_length=20, label="Teléfono", required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    postal_code = forms.CharField(max_length=10, label="Código Postal", required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    birth_date = forms.DateField(label="Fecha de Nacimiento",
        input_formats=['%Y-%m-%d'],  # Esto asegura que lo interprete bien
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    address = forms.CharField(label="Dirección", required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
    )

    # Campos de Member
    member_number = forms.IntegerField(label="Número de Socio",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    join_date = forms.DateField(label="Fecha de Ingreso",
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'value': datetime.date.today().isoformat()})
    )
    is_active = forms.BooleanField(label="Activo", required=False, initial=True)


'''
class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['member_number', 'join_date', 'is_active']
        
        widgets = {
            'join_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def save(self, commit=True):
        # Crear la persona
        person_data = {
            'names': self.cleaned_data.get('names'),
            'surnames': self.cleaned_data.get('surnames'),
            'dni': self.cleaned_data.get('dni'),
            'email': self.cleaned_data.get('email'),
            'phone': self.cleaned_data.get('phone'),
            'postal_code': self.cleaned_data.get('postal_code'),
            'birth_date': self.cleaned_data.get('birth_date'),
            'address': self.cleaned_data.get('address'),
        }

        # Los ** se usan en Python para desempaquetar un diccionario como argumentos de una función.
        person = Person.objects.create(**person_data)
        
        # Crear el usuario (puedes agregar más lógica para generar contraseñas o detalles)
        username = self.cleaned_data.get('dni')  # O cualquier campo único
        password = get_random_string(length=8)  # Contraseña temporal
        user = User.objects.create_user(username=username, password=password, email=person.email)
        
        # Crear el miembro
        member = super().save(commit=False)
        member.person = person
        member.save()

        return member
'''
'''
    # Cargar la persona relacionada
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['person'].queryset = Person.objects.filter()  # Puedes agregar un filtro si es necesario

    def clean_member_number(self):
        member_number = self.cleaned_data['member_number']
        if Member.objects.filter(member_number=member_number).exists():
            raise ValidationError("El número de socio ya está en uso.")
        return member_number
'''
