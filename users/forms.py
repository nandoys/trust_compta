from django import forms
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.translation import gettext_lazy as _

from accounting.models import FiscalYear


class EmailAwarePasswordResetTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        ret = super(EmailAwarePasswordResetTokenGenerator, self)._make_hash_value(
            user, timestamp
        )
        # sync_user_email_addresses(user)
        # email = user_email(user)
        # emails = set([email] if email else [])
        # emails.update(
        # EmailAddress.objects.filter(user=user).values_list("email", flat=True)
        # )
        # ret += "|".join(sorted(emails))
        return ret


# default_token_generator = EmailAwarePasswordResetTokenGenerator()


class PasswordVerificationMixin(object):
    def clean(self):
        cleaned_data = super(PasswordVerificationMixin, self).clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if (password1 and password2) and password1 != password2:
            self.add_error("password2", _("You must type the same password each time."))
        return cleaned_data


class PasswordField(forms.CharField):
    def __init__(self, *args, **kwargs):
        render_value = kwargs.pop(
            "render_value", False
        )
        kwargs["widget"] = forms.PasswordInput(
            render_value=render_value,
            attrs={"placeholder": kwargs.get("label")},
        )
        autocomplete = kwargs.pop("autocomplete", None)
        if autocomplete is not None:
            kwargs["widget"].attrs["autocomplete"] = autocomplete
        super(PasswordField, self).__init__(*args, **kwargs)


class SetPasswordField(PasswordField):
    def __init__(self, *args, **kwargs):
        kwargs["autocomplete"] = "new-password"
        super(SetPasswordField, self).__init__(*args, **kwargs)
        self.user = None


class LoginForm(forms.Form):
    login_widget = forms.TextInput(
        attrs={"placeholder": _("Username"), "autocomplete": "username"}
    )
    username = forms.CharField(
        label=_("Username"),
        widget=login_widget,
        max_length=50,
    )
    password = PasswordField(label=_("Password"), autocomplete="current-password")
    year = forms.ModelMultipleChoiceField(queryset=FiscalYear.objects.all(), label="Année exercice", widget=forms.widgets.Select(
                                            attrs={'class': 'form-select', 'id': 'year-field'}))
    remember = forms.BooleanField(label=_("Remember Me"), required=False)

    error_messages = {
        "account_inactive": _("This account is currently inactive."),
        "email_password_mismatch": _(
            "The e-mail address and/or password you specified are not correct."
        ),
        "username_password_mismatch": _(
            "The username and/or password you specified are not correct."
        ),
    }
