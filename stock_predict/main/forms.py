from django import forms

class home_form(forms.Form):
	date = forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'datepicker'}))