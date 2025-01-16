from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMessage, get_connection
from .models import ContactMessage

def contact_view(request):
    errors = {}
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        email_password = request.POST.get('email_password', '').strip()
        subject = request.POST.get('subject', '').strip()
        category = request.POST.get('category', '').strip()
        message = request.POST.get('message', '').strip()

        # Validation
        if not name:
            errors['name'] = "Full Name is required."
        if not email:
            errors['email'] = "Email Address is required."
        elif '@' not in email:
            errors['email'] = "Enter a valid email address."
        if not email_password:
            errors['email_password'] = "App Password is required."
        if not subject:
            errors['subject'] = "Subject is required."
        if not category:
            errors['category'] = "Category is required."
        if not message:
            errors['message'] = "Message is required."

        # If no errors, send the email and save to the database
        if not errors:
            try:
                # Create a connection with the user's credentials
                connection = get_connection(
                    username=email,
                    password=email_password,
                    fail_silently=False
                )
                email_message = EmailMessage(
                    subject=f"Contact Form Submission: {subject}",
                    body=f"Message from {name} ({email}):\n\n{message}\n\nCategory: {category}",
                    from_email=email,
                    to=["sportsystem305@gmail.com"],
                    connection=connection,
                )
                email_message.send()
                messages.success(request, "Thank you for your message! Your email has been sent.")

                # Save the form data to the database
                ContactMessage.objects.create(
                    name=name,
                    email=email,
                    subject=subject,
                    category=category,
                    message=message
                )
                return redirect('contact')  # Redirect to avoid form resubmission
            except Exception:
                messages.error(request, "We're sorry, but your message could not be sent. Please check your email password and try again.")
    return render(request, 'contact.html', {
        'errors': errors,
        'form_data': request.POST,
    })
