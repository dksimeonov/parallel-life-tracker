from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone


@shared_task
def send_welcome_email_task(username, email):
    subject = "Welcome to Parallel Life"
    message = (
        f"Hello {username},\n\n"
        f"Welcome to Parallel Life Tracker.\n"
        f"Your account was created successfully on {timezone.now():%Y-%m-%d %H:%M:%S}.\n\n"
        f"You can now create alternate life paths, milestones and reflections.\n\n"
        f"Best regards,\n"
        f"Parallel Life Tracker"
    )

    send_mail(
        subject=subject,
        message=message,
        from_email="noreply@parallellifetracker.local",
        recipient_list=[email],
        fail_silently=False,
    )

    return f"Welcome email sent to {email}"