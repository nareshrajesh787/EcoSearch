from django import forms


class homeForm(forms.Form):
  CHOICES = [
    ("1", "Precipitation Probability"),
    ("2", "Sunlight Exposure"),
    ("3" ," Temperature"),
    ("4", "Wind Speeds"),
    ("5", "Snowfall")
  ]

  address = forms.CharField(
    label="Enter your address here...",
    required=True,
    widget=forms.TextInput(attrs={"class": "form-control"})
  )
  data_type = forms.ChoiceField(
    label="Select a data type...",
    widget=forms.RadioSelect(),
    required=True,
    choices = CHOICES
  )
  