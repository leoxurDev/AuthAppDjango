from django.contrib import admin
from accounts.models import Profile, PortfolioImage

class PortfolioImageInline(admin.TabularInline):
    model = PortfolioImage
    extra = 1

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'location', 'template_choice')
    search_fields = ('user__username', 'title', 'bio')
    inlines = [PortfolioImageInline]

admin.site.register(PortfolioImage)
