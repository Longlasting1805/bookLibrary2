from django import forms
import datetime
from django.core.exceptions import validationError
from django.utils.translation import gettext_lazy as _

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text='Enter a date between now and 4 weeks (default 3).')

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        if data < datetime.date.today():
            raise validationError(_('Invalid date - renewal in past'))

        if data > datetime.date.today() + datetime.timedelta(weeks='4'):
            raise validationError(_('Invalid date - renewal more than 4 weeks ahead'))

        return data    
