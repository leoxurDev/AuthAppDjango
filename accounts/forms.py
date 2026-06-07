from django import forms
from accounts.models import Profile, PortfolioImage

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'title', 'bio', 'location', 'template_choice', 
            'primary_color', 'accent_color', 'font_family', 
            'profile_picture', 'banner_image', 
            'github_url', 'linkedin_url', 'twitter_url', 'website_url',
            'is_private'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell visitors about yourself...'}),
            'primary_color': forms.TextInput(attrs={'type': 'color'}),
            'accent_color': forms.TextInput(attrs={'type': 'color'}),
            'title': forms.TextInput(attrs={'placeholder': 'e.g. Full Stack Developer'}),
            'location': forms.TextInput(attrs={'placeholder': 'e.g. San Francisco, CA'}),
            'github_url': forms.URLInput(attrs={'placeholder': 'https://github.com/username'}),
            'linkedin_url': forms.URLInput(attrs={'placeholder': 'https://linkedin.com/in/username'}),
            'twitter_url': forms.URLInput(attrs={'placeholder': 'https://twitter.com/username'}),
            'website_url': forms.URLInput(attrs={'placeholder': 'https://yourwebsite.com'}),
        }

class PortfolioImageForm(forms.ModelForm):
    class Meta:
        model = PortfolioImage
        fields = ['image', 'title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Project Title'}),
            'description': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Brief description of this project...'}),
        }
