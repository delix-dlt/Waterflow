# leituras/forms.py
from django import forms

MOZ_PROVINCIAS = [
    ('', 'Selecione a Província'),
    ('Maputo Cidade', 'Maputo Cidade'),
    ('Maputo Província', 'Maputo Província'),
    ('Gaza', 'Gaza'),
    ('Inhambane', 'Inhambane'),
    ('Sofala', 'Sofala'),
    ('Manica', 'Manica'),
    ('Tete', 'Tete'),
    ('Zambézia', 'Zambézia'),
    ('Nampula', 'Nampula'),
    ('Cabo Delgado', 'Cabo Delgado'),
    ('Niassa', 'Niassa'),
]

class UserRegisterForm(forms.Form):
    nome_completo = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    telefone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    provincia = forms.ChoiceField(choices=MOZ_PROVINCIAS, widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_provincia'}))
    cidade = forms.CharField(widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_cidade'}), required=False)
    bairro = forms.CharField(widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_bairro'}), required=False)
    caixa_postal = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Opcional'}))

    class Meta:
        fields = ['nome_completo', 'telefone', 'provincia', 'cidade', 'bairro', 'caixa_postal']