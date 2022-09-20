from django import forms
from .models import USER_LIST




class MyForm(forms.Form):
	
	user = forms.MultipleChoiceField(
		required=True,
		widget=forms.CheckboxSelectMultiple,choices=USER_LIST)
 
	context1 = forms.CharField(
		required=True,
		widget=forms.Textarea(
			attrs={'placeholder': 'Context'}
		),
	)

	context2 = forms.CharField(
		required=True,
		widget=forms.Textarea(
			attrs={'placeholder': 'Context'}
		),
	)

	context3 = forms.CharField(
		required=True,
		widget=forms.Textarea(
			attrs={'placeholder': 'Context'}
		),
	)



'''
class MyForm(forms.Form):
    user = forms.MultipleChoiceField(
        required=True,
        widget=forms.MultipleChoiceField(
            choices=USER_LIST,
            attrs={'placeholder' : 'UserID'}
        ) 
    )
    group = forms.CharField(
        required=True,
        widget=forms.Select(
            choices=GROUP_LIST,
            attrs={'placeholder' : 'Group'}
        ) 
    )
    context = forms.CharField(
		required=True,
		widget=forms.TextInput(
			attrs={'placeholder': 'Context', 'maxlength': '500'}
		),
	)
'''

'''
class MyForm(forms.Form):
    	name = forms.CharField(
		required=True,
		widget=forms.TextInput(
			attrs={'placeholder': 'Name', 'maxlength': '100'}
		),
	)
	diet = forms.CharField(
		required=True,
		widget=forms.Select(choices=DIET_CHOICES, attrs={'placeholder': 'diet'}),
	)
	email = forms.EmailField(
		required=True,
		widget=forms.TextInput(attrs={'placeholder': 'Email', 'maxlength': '100'}),
	)
'''
