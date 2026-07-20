from django.conf import settings


def emailjs_keys(request):
    """Inyecta las claves de EmailJS en todos los templates."""
    return {
        "EMAILJS_PUBLIC_KEY":  getattr(settings, "EMAILJS_PUBLIC_KEY",  ""),
        "EMAILJS_SERVICE_ID":  getattr(settings, "EMAILJS_SERVICE_ID",  ""),
        "EMAILJS_TEMPLATE_ID": getattr(settings, "EMAILJS_TEMPLATE_ID", ""),
    }
