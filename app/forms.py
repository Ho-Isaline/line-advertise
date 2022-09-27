from turtle import width
from django import forms
from .models import USER_LIST

	
def on_button_pressed(self):
    self.botton.set_text("hi")

class MyForm(forms.Form):
	
	user = forms.MultipleChoiceField(
		required=True,
		widget=forms.CheckboxSelectMultiple,choices=USER_LIST)
 
	context = forms.CharField(
		required=True,
		widget=forms.Textarea(
			attrs={'placeholder': 'Context'}
		),
	)

 
 

'''

class MyApp(App):
    
	def __init__(self, *args):
		super(MyApp, self).__init__(*args)
	def main(self):
		container = gui.VBox(width=300, height=300)
		self.bt = gui.Button("+")
		#setting the listener for the onclick event of the button
		self.bt.onclick.do(self.on_button_pressed)
		container.append(self.bt)
		return container

	def on_button_pressed(self, widgit):
		self.bt.set_text('Hi!')
'''


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
