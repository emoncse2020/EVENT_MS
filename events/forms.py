from django import forms
from events.models import Event, Participant, Category

class StyledFormMixin:
    default_classes = "w-full p-2 border rounded focus:ring-2 focus:ring-blue-500 focus:border-blue-500"

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.EmailInput)):
                field.widget.attrs.update({
                    'class' : self.default_classes,
                    'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class' : self.default_classes,
                    'placeholder': f"Enter {field.label.lower()}",
                    'rows':3
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class': 'p-2 border rounded',
                    'type': 'date'
                    
                })
            elif isinstance(field.widget, forms.TimeInput):
                field.widget.attrs.update({
                    # 'class':"p-2 border rounded",
                    'type': 'time'
                    
                })


class EventModelForm(StyledFormMixin,forms.ModelForm):

    category = forms.ModelChoiceField(
        queryset= Category.objects.all(),
        empty_label= "Select a Category",
        widget= forms.Select(attrs={
            'class' : "p-2 border rounded"
        })
      
    )
    
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time', 'location', 'category']
        widgets = {
            'date': forms.SelectDateWidget,
            'time': forms.TimeInput
        }
       

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()


class ParticipantModelForm(StyledFormMixin,forms.ModelForm):
    
    class Meta:
        model = Participant
        fields = ['name', 'email']
        # widgets = {
        #     'name': forms.TextInput(attrs={
        #         'class': 'w-full p-2 border rounded'
        #     }), 
        #     'email': forms.EmailInput(attrs={
        #         'class':"w-full p-2 border rounded" 
        #     })
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()


class CategoryModelForm(forms.ModelForm):
    
    class Meta:
        model = Category
        fields = ['name', 'description']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': "w-full p-2 border rounded"
            }),
            'description': forms.Textarea(attrs={
                "class": "w-full p-2 border rounded", 'rows':3
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

