from decimal import Decimal
from django.contrib import messages
from django.shortcuts import render, redirect
from models import Player
from forms import PlayerForm, TransferForm, IncomeForm, get_transfer_choices

STARTING_BALANCE = 1500


def index(request):
    return render(request, "index.html")


def new_player(request):
    if request.method == 'POST':
        pf = PlayerForm(request.POST)
        if pf.is_valid():
            new_p = pf.save(commit=False)
            new_p.balance = STARTING_BALANCE
            new_p.save()
            return redirect('bank.views.player', new_p.id)
    else:
        pf = PlayerForm()

    return render(request, "new_player.html", {'form': pf})


def do_transfer(from_player_id, to_player_id, amount):
    if from_player_id != 'bank':
        from_player = Player.objects.get(id=from_player_id)
        from_player.balance -= amount
        from_player.save()

    if to_player_id != 'bank':
        to_player = Player.objects.get(id=to_player_id)
        to_player.balance += amount
        to_player.save()

        return to_player.name

    return to_player_id


def player(request, player_id):
    player_id = int(player_id)
    p = Player.objects.get(id=player_id)

    if request.method == 'POST' and request.POST['form_name'] == 'transfer':
        tf = TransferForm(request.POST)
        tf.fields['to'].choices = get_transfer_choices(player_id)
        if tf.is_valid():
            to_name = do_transfer(player_id, tf.cleaned_data['to'], Decimal(tf.cleaned_data['amount']))
            messages.success(request, "${} transferred to {}.".format(tf.cleaned_data['amount'], to_name))
            return redirect('bank.views.player', player_id)
        iform = IncomeForm()
    elif request.method == 'POST' and request.POST['form_name'] == 'income':
        iform = IncomeForm(request.POST)
        if iform.is_valid():
            p.balance += Decimal(iform.cleaned_data['amount'])
            p.save()
            messages.success(request, "Added ${} income..".format(iform.cleaned_data['amount']))
            return redirect('bank.views.player', player_id)
        tf = TransferForm()
    else:
        tf = TransferForm()
        iform = IncomeForm()
        tf.fields['to'].choices = get_transfer_choices(player_id)

    return render(request, "player.html", {'player': p, 'transfer_form': tf, 'players': Player.objects.all(),
                                           'income_form': iform})


def pass_go(request):
    if request.method != 'POST':
        raise ValueError("Must be post")

    p = Player.objects.get(id=request.POST['player_id'])
    p.balance += 200
    p.save()
    messages.success(request, "Have $200 {}".format(p.name))
    return redirect('bank.views.player', p.id)


def reset(request):
    for p in Player.objects.all():
        p.delete()
    return redirect('/')
