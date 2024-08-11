from django import forms
from .models import Empresas
from django.core.exceptions import ValidationError


class EmpresaForm(forms.ModelForm):
    estagio = forms.MultipleChoiceField(
        choices=Empresas.estagio_choices,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        label="Qual o estágio da empresa?"
    )

    class Meta:
        model = Empresas
        fields = [
            'nome',
            'cnpj',
            'site',
            'tempo_existencia',
            'descricao',
            'data_final_captacao',
            'percentual_equity',
            'estagio',
            'area',
            'publico_alvo',
            'valor',
            'pitch',
            'logo',
        ]
        widgets = {
            'nome': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Digite o nome da sua empresa ...'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o seu CNPJ ...'}),
            'site': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Digite o seu site ...'}),
            'tempo_existencia': forms.Select(attrs={'class': 'form-select'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descreva a sua empresa ...'}),
            'data_final_captacao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'percentual_equity': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Porcentagem de equity'}),
            'area': forms.Select(attrs={'class': 'form-select'}),
            'publico_alvo': forms.Select(attrs={'class': 'form-select'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Valor total a ser captado'}),
            'pitch': forms.FileInput(attrs={'class': 'form-control'}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj')
        if len(cnpj) != 14:
            raise ValidationError('CNPJ inválido. Deve conter 14 dígitos.')
        return cnpj

    def clean_valor(self):
        valor = self.cleaned_data.get('valor')
        if valor <= 0:
            raise ValidationError('O valor deve ser um número positivo.')
        return valor

    def clean_logo(self):
        logo = self.cleaned_data.get('logo')
        if logo and logo.size > 100 * 1024 * 1024:
            raise ValidationError('A logo não pode exceder 100MB.')
        return logo

    def clean_pitch(self):
        pitch = self.cleaned_data.get('pitch')
        if pitch and pitch.size > 100 * 1024 * 1024:
            raise ValidationError('O pitch não pode exceder 100MB.')
        return pitch

    def clean_estagio(self):
        estagio = self.cleaned_data.get('estagio')
        if estagio:
            return ','.join(estagio)  # Concatenate selected values into a string
        return estagio
