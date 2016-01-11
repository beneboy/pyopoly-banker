from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from models import Player


def get_transfer_choices(player_id):
    players = Player.objects.all()
    player_list = [('bank', 'Bank')]
    for player in players:
        if player.id != player_id:
            player_list.append((player.id, player.name))
    return player_list


class TransferForm(forms.Form):
    amount = forms.FloatField()
    to = forms.ChoiceField(label='Transfer To', choices=[])
    
    def __init__(self, *args, **kwargs):
        super(TransferForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Transfer'))

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError("Amount must be > 0.")
        return amount


class IncomeForm(forms.Form):
    amount = forms.FloatField()

    def __init__(self, *args, **kwargs):
        super(IncomeForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Income'))

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError("Amount must be > 0.")
        return amount


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super(PlayerForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))
