from datetime import date
from django import forms
import re
from django.core.exceptions import ValidationError
class DateSelectorWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        days = [(day, day) for day in range(10, 22)]
        months = [('ARID','ARID')]

        widgets = [
            forms.TextInput(attrs={'size':4, 'max_length':4}),
            forms.Select(attrs=attrs, choices=months),
            forms.Select(attrs=attrs, choices=days),

        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if isinstance(value, date):
            return [value.day, value.month, value.year]
        elif isinstance(value, str):
            year, month, day = value.split('-')
            return [day, month, year]
        return [None, None, None]

    def value_from_datadict(self, data, files, name):
        day, month, year = super().value_from_datadict(data, files, name)
        # DateField expects a single string that it can parse into a date.
        return '{}-{}-{}'.format(year, month, day)
def check_n(value):
    string = value[8:]
    print(string)
    if not re.findall('[0-9]+', string):
        raise ValidationError('Check Arid Number Format')

class EnrollForm(forms.ModelForm):
    Arid_no = forms.CharField(widget=DateSelectorWidget(), validators=[check_n])
