import re

from django.contrib.auth import get_user_model
from django.core import mail
from django.core.mail import send_mail
from django.test import TestCase, override_settings
from django.urls import reverse

User = get_user_model()


class PasswordResetFlowTests(TestCase):

    def setUp(self):
        self.email = "testuser@example.com"
        self.password = "OldPass123!"
        self.user = User.objects.create_user(
            username=self.email,
            email=self.email,
            password=self.password,
        )

    def test_password_reset_page_loads(self):
        response = self.client.get(reverse("password_reset"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Recuperar contraseña")

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_password_reset_email_is_sent_for_registered_user(self):
        response = self.client.post(reverse("password_reset"), {"email": self.email})
        self.assertRedirects(response, reverse("password_reset_done"))
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(self.email, mail.outbox[0].to)
        self.assertIn("restablecer tu contraseña", mail.outbox[0].subject.lower())

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_password_reset_link_opens_and_allows_new_password(self):
        self.client.post(reverse("password_reset"), {"email": self.email})
        self.assertEqual(len(mail.outbox), 1)

        # Construct a valid reset path directly using Django token generator
        from django.utils.http import urlsafe_base64_encode
        from django.utils.encoding import force_bytes
        from django.contrib.auth.tokens import default_token_generator

        uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        reset_path = reverse("password_reset_confirm", kwargs={"uidb64": uidb64, "token": token})
        # Django may redirect the initial GET to a normalized 'set-password' URL (302),
        # so follow redirects to reach the final form page and assert 200.
        response = self.client.get(reset_path, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nueva contraseña")

        # If Django redirected to a normalized 'set-password' path, post there
        post_path = reset_path
        if response.redirect_chain:
            post_path = response.redirect_chain[-1][0]

        response = self.client.post(
            post_path,
            {
                "new_password1": "NewPass123!",
                "new_password2": "NewPass123!",
            },
            follow=True,
        )
        # Follow redirects; assert final response OK (password change verified below)
        self.assertEqual(response.status_code, 200)

        # Verify the user's password was actually updated
        user = User.objects.get(email=self.email)
        self.assertTrue(user.check_password("NewPass123!"))

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_direct_send_mail_works(self):
        send_mail(
            "Prueba de envío",
            "Este es un correo de prueba.",
            "noreply@cap-online.onrender.com",
            [self.email],
            fail_silently=False,
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Prueba de envío")
        self.assertIn(self.email, mail.outbox[0].to)
