from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import (
    ClubInfo, ClubBoard, AuditCommittee,
    Person, Member, Discipline, DisciplineCommittee, Enrollment, 
    Article, ArticleImage,
)


@admin.register(ClubInfo)
class ClubInfoAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Sólo permitir un único registro
        return not ClubInfo.objects.exists()

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('surnames', 'names', 'dni', 'email')
    search_fields = ('surnames', 'names', 'dni', 'email')
    readonly_fields = ('profile_picture',)

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('member_number', 'person', 'join_date', 'is_active')
    search_fields = ('member_number', 'person__surnames', 'person__dni')

@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    list_display = ('name', 'days_and_times')
    search_fields = ('name',)

@admin.register(DisciplineCommittee)
class DisciplineCommitteeAdmin(admin.ModelAdmin):
    list_display = ('discipline', 'president', 'secretary', 'treasurer')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('member', 'discipline', 'enrolled_at')
    search_fields = ('member__person__surnames', 'discipline__name')

class ArticleImageInline(admin.TabularInline):
    model = ArticleImage
    extra = 1

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publish_date')
    inlines = [ArticleImageInline]
    search_fields = ('title', 'author__surnames')

@admin.register(ClubBoard)
class ClubBoardAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Solo permitir agregar si no existe ya una instancia
        return not ClubBoard.objects.exists()

@admin.register(AuditCommittee)
class AuditCommitteeAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # De momento permitimos más de uno, pero podrías limitarlo igual que ClubBoard
        return super().has_add_permission(request)



# Crear un formulario de usuario personalizado
class CustomUserCreationForm(UserCreationForm):
    dni = forms.CharField(max_length=20, required=True)
    birth_date = forms.DateField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_dni(self):
        dni = self.cleaned_data['dni']
        if Person.objects.filter(dni=dni).exists():
            raise forms.ValidationError("Ya existe una persona con este DNI.")
        return dni

class CustomUserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    list_display = ('username', 'first_name', 'last_name', 'email')
    search_fields = ('username', 'email')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'dni', 'birth_date'),
        }),
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:
            Person.objects.create(
                user=obj,
                names=obj.first_name,
                surnames=obj.last_name,
                email=obj.email,
                dni=form.cleaned_data['dni'],
                birth_date=form.cleaned_data['birth_date'],
            )

# Registra la configuración personalizada del admin de User
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)