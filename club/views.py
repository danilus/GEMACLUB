from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from .forms import MemberWithPersonForm
from .models import Person, Member

import random
import string


def generate_random_password(length=10):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


@login_required
@permission_required('club.dashboard', raise_exception=True)
def dashboard(request):
    return render(request, 'club/dashboard.html', {})


### SOCIOS ###

@login_required
@permission_required('club.member_list', raise_exception=True)
def member_list(request):
    members = Member.objects.select_related('person').order_by('member_number')
    return render(request, 'club/member_list.html', {'members': members})

@login_required
@permission_required('club.member_create', raise_exception=True)
def member_create(request):
    if request.method == 'POST':
        form = MemberWithPersonForm(request.POST)

        if form.is_valid():
            try:
                # Extraer datos de Person
                names = form.cleaned_data['names']
                surnames = form.cleaned_data['surnames']
                dni = form.cleaned_data['dni']
                email = form.cleaned_data['email']
                phone = form.cleaned_data['phone']
                postal_code = form.cleaned_data['postal_code']
                birth_date = form.cleaned_data['birth_date']
                address = form.cleaned_data['address']

                # Crear usuario básico
                username = f"{dni}"
                default_password = generate_random_password()
                user = User.objects.create_user(username=username, email=email, password=default_password)
                user.first_name = names
                user.last_name = surnames
                user.save()

                # Crear Person
                person = Person(
                    user=user,
                    names=names,
                    surnames=surnames,
                    dni=dni,
                    email=email,
                    phone=phone,
                    postal_code=postal_code,
                    birth_date=birth_date,
                    address=address
                )
                person.full_clean()
                person.save()

                # Crear Member
                member = Member(
                    person=person,
                    member_number=form.cleaned_data['member_number'],
                    join_date=form.cleaned_data['join_date'],
                    is_active=form.cleaned_data['is_active']
                )
                member.full_clean()
                member.save()

                messages.success(
                    request,
                    f'Socio N° {member.member_number} ({member.person.get_full_name()}) creado correctamente / '
                    f'Usuario: {user.username} / Contraseña: {default_password}'
                )
                return redirect('club:member_list')

            except ValidationError as e:
                form.add_error(None, e)  # Agrega los errores generales al form
                messages.error(request, "Ocurrió un error en la validación al intentar crear el socio.")

    else:
        form = MemberWithPersonForm()

    return render(request, 'club/member_form.html', {
        'form': form
    })

@login_required
@permission_required('club.member_edit', raise_exception=True)
def member_edit(request, pk):
    member = get_object_or_404(Member, pk=pk)
    person = member.person

    if request.method == 'POST':
        form = MemberWithPersonForm(request.POST)
        if form.is_valid():
            try:
                # Actualizar Person
                person.names = form.cleaned_data['names']
                person.surnames = form.cleaned_data['surnames']
                person.dni = form.cleaned_data['dni']
                person.email = form.cleaned_data['email']
                person.phone = form.cleaned_data['phone']
                person.postal_code = form.cleaned_data['postal_code']
                person.birth_date = form.cleaned_data['birth_date']
                person.address = form.cleaned_data['address']
                person.full_clean()  # <-- Esto activa validaciones del modelo
                person.save()

                # Actualizar User (opcional pero recomendado)
                if person.user:
                    user = person.user
                    user.first_name = person.names
                    user.last_name = person.surnames
                    user.email = person.email
                    user.save()

                # Actualizar Member
                member.member_number = form.cleaned_data['member_number']
                member.join_date = form.cleaned_data['join_date']
                member.is_active = form.cleaned_data['is_active']
                member.full_clean()  # <-- Por si agregás validaciones ahí también
                member.save()

                messages.success(request, f'Socio/a #{member.member_number} actualizado/a correctamente.')
                return redirect('club:member_list')

            except ValidationError as e:
                form.add_error(None, e)  # Agrega errores no específicos al form
                messages.error(request, "Error de validación en el modelo. Por favor revisá los datos ingresados.")
        else:
            messages.error(request, "Ocurrió un error en el formulario.")
    else:
        initial = {
            'names': person.names,
            'surnames': person.surnames,
            'dni': person.dni,
            'email': person.email,
            'phone': person.phone,
            'postal_code': person.postal_code,
            'birth_date': person.birth_date.strftime('%Y-%m-%d') if person.birth_date else '',
            'address': person.address,
            'member_number': member.member_number,
            'join_date': member.join_date.strftime('%Y-%m-%d') if member.join_date else '',
            'is_active': member.is_active,
        }
        form = MemberWithPersonForm(initial=initial)

    return render(request, 'club/member_form.html', {
        'form': form,
        'editing': True,
        'member': member
    })

@login_required
@permission_required('club.delete_member', raise_exception=True)
def member_delete(request, pk):
    member = get_object_or_404(Member, pk=pk)

    if request.method == 'POST':
        full_name = member.person.get_full_name()
        member_number = member.member_number
        member.delete()  # Ahora esto borra todo: Member → Person → User

        messages.success(request, f'Socio N° {member_number} ({full_name}) eliminado correctamente.')
        return redirect('club:member_list')