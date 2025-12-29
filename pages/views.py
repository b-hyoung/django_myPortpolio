from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .forms import ContactForm

def about(request):
    return render(request,"pages/about.html", {'show_hero_section': False})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            try:
                # Send email - uses settings from mysite/settings.py
                send_mail(
                    f'Contact Form: {subject} from {name}', # Email subject
                    f'From: {name} ({email})\n\nMessage:\n{message}', # Email body
                    email, # From email (should be a configured EMAIL_HOST_USER for production)
                    ['your_email@example.com'], # To email - replace with actual recipient
                    fail_silently=False,
                )
                messages.success(request, 'Thank you for your message! We will get back to you soon.')
                return redirect('contact') # Redirect to prevent resubmission
            except Exception as e:
                messages.error(request, f'An error occurred while sending your message. Please try again later. ({e})')
    else:
        form = ContactForm()
    
    return render(request,"pages/contact.html", {'form': form})
