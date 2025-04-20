from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from datetime import date


# Validador personalizado para imágenes
# Verifica el tamaño máximo y el tipo de archivo permitido (JPEG o PNG)
def validate_image(image):
    file_size = image.size
    limit_mb = 2
    if file_size > limit_mb * 1024 * 1024:
        raise ValidationError("La imagen no puede pesar más de 2MB.")

    # Solo validamos el content_type si está disponible
    content_type = getattr(image, 'content_type', None)
    if content_type and content_type not in ['image/jpeg', 'image/png']:
        raise ValidationError("Solo se permiten imágenes JPEG o PNG.")


class ClubInfo(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='club/logo/', null=True, blank=True)
    description = models.TextField(blank=True)
    full_description = models.TextField(blank=True)
    statute = models.FileField(upload_to='club/statute/', null=True, blank=True)

    class Meta:
        verbose_name = "Información del Club"
        verbose_name_plural = "Información del Club"

    def __str__(self):
        return self.name
    

class Person(models.Model):
    # Representa una persona genérica del club (socio, empleado, entrenador, etc.)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    names = models.CharField(max_length=100)
    surnames = models.CharField(max_length=100)
    dni = models.CharField(
        max_length=20, unique=True,
        validators=[RegexValidator(regex=r'^\d+$', message='El DNI solo debe contener números')]
    )
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    postal_code = models.CharField(max_length=10, null=True, blank=True)
    birth_date = models.DateField()
    address = models.TextField(null=True, blank=True)
    # Usamos una imagen predeterminada si no se proporciona ninguna foto de perfil
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', 
        blank=True, 
        null=True, 
        default='profile_pictures/default_profile_picture.jpg',  # Imagen predeterminada
        validators=[validate_image]  # Valida tipo y tamaño
    )

    def __str__(self):
        return f"{self.surnames}, {self.names}"

    def get_full_name(self):
        return f"{self.names} {self.surnames}"

    def get_age(self):
        if self.birth_date:
            today = date.today()
            age = today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
            return age
        return None
    
'''
@receiver(post_save, sender=User)
def create_or_update_person(sender, instance, created, **kwargs):
    if created:
        Person.objects.create(user=instance, names=instance.first_name, surnames=instance.last_name, email=instance.email, birth_date="1900-01-01")
    else:
        person = getattr(instance, 'person', None)
        if person:
            person.email = instance.email
            person.names = instance.first_name
            person.surnames = instance.last_name
            person.save()
'''

class Member(models.Model):
    # Representa a un socio del club
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    member_number = models.PositiveIntegerField(unique=True)
    join_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"N° {self.member_number} - {self.person}"

    def delete(self, *args, **kwargs):
        # Guardamos la referencia antes de eliminar el Member
        person = self.person
        user = person.user if person else None

        super().delete(*args, **kwargs)  # Elimina el Member

        if user:
            user.delete()
        if person:
            person.delete()
            

class ClubBoard(models.Model):
    # Comisión Directiva del club, con vocales ordenados
    president = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='club_president')
    secretary = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='club_secretary')
    treasurer = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='club_treasurer')
    vocal_1 = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='club_vocal_1')
    vocal_2 = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='club_vocal_2')
    vocal_3 = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='club_vocal_3')
    suplente_1 = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='club_suplente_1')
    suplente_2 = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='club_suplente_2')

    def clean(self):
        if ClubBoard.objects.exists() and not self.pk:
            raise ValidationError("Ya existe una Comisión Directiva. Solo puede haber una.")
    
    def __str__(self):
        return "Comisión Directiva"
    
class AuditCommittee(models.Model):
    # Comisión Revisora de Cuentas
    titular_1 = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='audit_titular_1')
    titular_2 = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='audit_titular_2')
    titular_3 = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='audit_titular_3')
    suplente = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='audit_suplente')
    

class Discipline(models.Model):
    # Representa una disciplina deportiva del club
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    days_and_times = models.CharField(max_length=200)
    coaches = models.ManyToManyField(Person, related_name='disciplines_as_coach', blank=True)

    def __str__(self):
        return self.name

class DisciplineCommittee(models.Model):
    # Subcomisión de una disciplina, compuesta por miembros del club
    discipline = models.OneToOneField(Discipline, on_delete=models.CASCADE)
    president = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='president_of_discipline')
    secretary = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='secretary_of_discipline')
    treasurer = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='treasurer_of_discipline')
    vocal_1 = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='vocal1_of_discipline')
    vocal_2 = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='vocal2_of_discipline')

class Enrollment(models.Model):
    # Inscripción de un miembro a una disciplina, única por combinación
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['member', 'discipline'], name='unique_enrollment')
        ]


class Article(models.Model):
    # Publicación de noticias del club
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True)
    publish_date = models.DateField()  # Se puede diferenciar de created_at
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-publish_date']

    def __str__(self):
        return self.title

class ArticleImage(models.Model):
    # Permite múltiples imágenes por noticia
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='article_images/', validators=[validate_image])