from django.contrib import admin
from django import forms
from .models import Project
import base64
from PIL import Image
from io import BytesIO
import logging

logger = logging.getLogger(__name__)

class ProjectAdminForm(forms.ModelForm):
    image = forms.ImageField(required=False, label='이미지 업로드')

    class Meta:
        model = Project
        fields = '__all__'
        widgets = {
            'image_data': forms.Textarea(attrs={'readonly': 'readonly', 'rows': 5}),
        }

class ProjectAdmin(admin.ModelAdmin):
    form = ProjectAdminForm
    list_display = ('title', 'created_at', 'is_visible')
    
    def save_model(self, request, obj, form, change):
        uploaded_image = form.cleaned_data.get('image')
        if uploaded_image:
            try:
                logger.info(f"Processing uploaded image: {uploaded_image.name}, original size: {uploaded_image.size} bytes")

                # Open the image using Pillow
                img = Image.open(uploaded_image)
                
                # Define max size and resize the image
                max_size = (1200, 1200)
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                # Save the resized image to an in-memory buffer
                buffer = BytesIO()
                # Use the original format, or a default like JPEG if the format is not available
                image_format = img.format if img.format in ['JPEG', 'PNG', 'GIF'] else 'JPEG'
                img.save(buffer, format=image_format)
                image_bytes = buffer.getvalue()
                
                logger.info(f"Resized image size: {len(image_bytes)} bytes")

                # Encode the resized image in Base64
                encoded_image = base64.b64encode(image_bytes).decode('utf-8')
                
                # Determine the MIME type
                mime_type = f'image/{image_format.lower()}'
                data_uri = f"data:{mime_type};base64,{encoded_image}"

                obj.image_data = data_uri
            except Exception as e:
                logger.error(f"Error processing image: {e}", exc_info=True)
                # Optionally, you could add a message to the user
                # self.message_user(request, "Error processing image.", level='error')

        super().save_model(request, obj, form, change)

admin.site.register(Project, ProjectAdmin)