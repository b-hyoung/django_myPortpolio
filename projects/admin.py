from django.contrib import admin
from django import forms
from .models import Project
import base64

class ProjectAdminForm(forms.ModelForm):
    # This is a temporary field to handle the image upload in the admin UI.
    # It is not saved to the database directly.
    image = forms.ImageField(required=False, label='이미지 업로드')

    class Meta:
        model = Project
        fields = '__all__'
        # Exclude the 'image_data' field from the form's direct editing if you want,
        # but including it can be useful for debugging.
        # It's better to show it as read-only.
        widgets = {
            'image_data': forms.Textarea(attrs={'readonly': 'readonly', 'rows': 5}),
        }

class ProjectAdmin(admin.ModelAdmin):
    form = ProjectAdminForm
    
    # It's good practice to show which fields are displayed in the list view
    list_display = ('title', 'created_at', 'is_visible')
    
    def save_model(self, request, obj, form, change):
        # Check if a new image file has been uploaded
        uploaded_image = form.cleaned_data.get('image')
        if uploaded_image:
            # Read the file's content
            image_bytes = uploaded_image.read()
            # Encode it in Base64
            encoded_image = base64.b64encode(image_bytes).decode('utf-8')
            # Get the content type and create the data URI
            mime_type = uploaded_image.content_type
            data_uri = f"data:{mime_type};base64,{encoded_image}"
            # Save the data URI to the model's text field
            obj.image_data = data_uri
            
        # Call the parent class's save_model method to save the object
        super().save_model(request, obj, form, change)

admin.site.register(Project, ProjectAdmin)