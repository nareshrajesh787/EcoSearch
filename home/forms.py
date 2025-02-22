from django import forms


class homeForm(forms.Form):
  CHOICES = [
    ("1", "Ocean"),
    ("2", "Air Quality"),
    ("3" ," Temperature")
  ]

  address = forms.CharField(
    label="Enter your address here...",
    required=True,
    widget=forms.TextInput(attrs={"class": "form-control"})
  )
  data_type = forms.ChoiceField(
    widget=forms.RadioSelect(),
    required=True,
    choices = CHOICES
  )
  