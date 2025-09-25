
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from datetime import date


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(default=date.today, null=False, blank=False)
    birth_date_edited = models.BooleanField(default=False)
    def user_profile_image_path(instance, filename):
        # File will be uploaded to MEDIA_ROOT/profile_images/<slug>/<filename>
        return f'profile_images/{instance.slug}/{filename}'

    profile_img = models.ImageField(upload_to=user_profile_image_path, default='blank_profile.png')
    date_modified = models.DateTimeField(User, auto_now=True)
    slug = models.SlugField(unique=True, blank=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.user.username)
            slug = base_slug
            num = 1
            while Profile.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.slug = slug
        if self.pk is not None:
            old = Profile.objects.get(pk=self.pk)
            if old.birth_date != self.birth_date and old.birth_date_edited:
                self.birth_date = old.birth_date
            elif old.birth_date != self.birth_date:
                self.birth_date_edited = True
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username

# Create a Profile when new user Signs up
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance, birth_date=date.today())
        user_profile.save()
