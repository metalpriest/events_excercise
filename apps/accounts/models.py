from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _

from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)

    # Django is quite coupled with username as far as I know.
    # To don't have a mess with migrations and auth backends
    # I've decided to keep it and more concentrate on business logic of exercise and test coverage
    # Anyway it can be removed later
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Use email as username login'),
        validators=[validate_email],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    def get_short_name(self):
        return self.username.split('@')[0]
    
    def save(self, *args, **kwargs):
        self.email = self.username
        super(User, self).save(*args, **kwargs)
