from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

TEMPLATE_CHOICES = [
    ('material', 'Material Theme'),
    ('dark_cyber', 'Cyberpunk Glow'),
    ('glassmorphism', 'Glassmorphism'),
    ('minimalist', 'Minimalist Clean'),
]

FONT_CHOICES = [
    ('Roboto', 'Roboto (Clean/Modern)'),
    ('Inter', 'Inter (Sleek/Tech)'),
    ('Playfair Display', 'Playfair Display (Elegant/Serif)'),
    ('Fira Code', 'Fira Code (Developer/Monospace)'),
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    title = models.CharField(max_length=100, blank=True, default="My Portfolio Profile")
    bio = models.TextField(blank=True, default="Welcome to my custom profile! You can edit this bio in your dashboard.")
    location = models.CharField(max_length=100, blank=True, default="Earth")
    
    # Custom design styles
    template_choice = models.CharField(max_length=20, choices=TEMPLATE_CHOICES, default='material')
    primary_color = models.CharField(max_length=7, default='#3f51b5') # Hex color (e.g. Indigo)
    accent_color = models.CharField(max_length=7, default='#ff4081') # Hex color (e.g. Pink)
    font_family = models.CharField(max_length=50, choices=FONT_CHOICES, default='Roboto')
    is_private = models.BooleanField(default=False)
    
    # Images
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    banner_image = models.ImageField(upload_to='banners/', blank=True, null=True)
    
    # Social links
    github_url = models.URLField(blank=True, default='')
    linkedin_url = models.URLField(blank=True, default='')
    twitter_url = models.URLField(blank=True, default='')
    website_url = models.URLField(blank=True, default='')
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

class PortfolioImage(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='portfolio_images/')
    title = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or f"Image for {self.profile.user.username}"

# Automatically create a profile when a User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Check if profile exists before saving (to handle case where database is created/migrated without signals initially or for admin user creation)
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        Profile.objects.create(user=instance)
