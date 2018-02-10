from django import forms

class SearchForm(forms.Form):
	keyword = forms.CharField(label='', max_length=255, required = True, 
								widget=forms.TextInput(attrs={
									'class': 'search-keyword',
									}))

class ContactForm(forms.Form):
	message = forms.CharField(widget=forms.Textarea(attrs={
									'class':'mensaje',
									'rows':1,
									'value':'MESSAGE:'
									}),max_length=200)
	name = forms.CharField(widget=forms.TextInput(attrs={
									'class': 'nombre',
									'value':'NAME:',
									}),max_length=100)
	sender = forms.EmailField(widget=forms.TextInput(attrs={
									'class': 'email',
									'value':'E-MAIL:',
									}),)
	subject = forms.CharField(widget=forms.TextInput(attrs={
									'class': 'asunto',
									'value':'SUBJECT:',
									}),max_length=100)
	cc_myself = forms.BooleanField(required=False)
	

# class ContactForm(forms.Form):
#     subject = forms.CharField(max_length=100)
#     message = forms.CharField(widget=forms.Textarea)
#     sender = forms.EmailField()
#     cc_myself = forms.BooleanField(required=False)