from django.contrib.auth.forms import PasswordChangeForm


class ChangePasswordForm(PasswordChangeForm):
  """
    Form that overrides Django's PasswordChangeForm.
    widget.attrs are used to specify custom CSS classes and placeholders.
  """
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.fields['old_password'].widget.attrs.update({
        'class': 'form-control',
        'placeholder': 'Please enter your current password',
        'id': 'old_password',
        'required': True,
    })
    
    self.fields['new_password1'].widget.attrs.update({
        'class': 'form-control',
        'placeholder': 'Please enter a new password',
        'id': 'new_password1',
        'required': True,
    })
    
    self.fields['new_password2'].widget.attrs.update({
        'class': 'form-control',
        'placeholder': 'Please confirm your new password',
        'id': 'new_password2',
        'required': True,
    })