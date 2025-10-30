from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from accounts.models import Profile
from accounts.models import Role

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    try:
        # Always ensure the "Student" role exists
        student_role, _ = Role.objects.get_or_create(name='Student')

        if created:
            # Create a profile for the new user
            Profile.objects.get_or_create(
                user=instance,
                defaults={
                    'first_name': instance.first_name,
                    'last_name': instance.last_name,
                    'role': student_role,
                }
            )
        else:
            # Update or ensure an existing profile
            profile, _ = Profile.objects.get_or_create(user=instance)
            profile.first_name = instance.first_name
            profile.last_name = instance.last_name

            # Assign role if missing
            if not profile.role:
                profile.role = student_role

            profile.save()

    except Exception:
        # Silently ignore any signal errors to avoid blocking user save
        pass