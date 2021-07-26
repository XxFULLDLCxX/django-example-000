from django import forms
from django.forms import ModelForm
from .models import Contacto, Person, Pregunta, Respuesta, PreguntasRespondidas

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import get_user_model, authenticate

User = get_user_model()


class ContactoForm(ModelForm):
    class Meta:
        model = Contacto
        fields = ['nome', 'apelido', 'email', 'telefone', 'data_de_nacimento']


class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = ['nome', 'apelido', 'email']


class ElegirInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super(ElegirInlineFormSet, self).clean()

        answer_correct = 0
        for form in self.forms:
            if not form.is_valid():
                return
            if form.cleaned_data and form.cleaned_data.get("correct") is True:
                answer_correct += 1
        try:
            assert answer_correct == Pregunta.possible_answer
        except AssertionError:
            raise forms.ValidationError("Solamente una Respuesta Correcta ")


class UsuarioLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("User is Not Found.")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect Password.")
            if not user.is_active:
                raise forms.ValidationError("User is Not Active.")

        return super(UsuarioLoginForm, self).clean(*args, **kwargs)


class RegistroForm(UserCreationForm):
    nome = forms.CharField(max_length=25, required=True)
    apelido = forms.CharField(max_length=25, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User

        fields = [
            'nome',
            'apelido',
            'username',
            'email',
            'password1',
            'password2',
        ]