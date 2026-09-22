"""
finance/views.py
Todas las vistas están protegidas con @role_required('super_admin'):
sólo Cristian gestiona ingresos y contrataciones globales.
"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.shortcuts import render, redirect, get_object_or_404

from accounts.decorators import role_required
from core.utils import log_activity
from .forms import IncomeForm, ContractForm
from .models import Income, Contract


@login_required
@role_required("super_admin")
def income_list(request):
    if request.method == "POST":
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save()
            log_activity(request.user, "income_created", {"income_id": income.id})
            messages.success(request, "Ingreso registrado.")
            return redirect("finance:income_list")
    else:
        form = IncomeForm()

    incomes = Income.objects.all()
    totals = incomes.aggregate(
        total=Sum("amount"),
        pagado=Sum("amount", filter=Q(status=Income.Status.PAID)),
        pendiente=Sum("amount", filter=Q(status=Income.Status.PENDING)),
    )
    return render(request, "dashboard/income.html", {
        "incomes": incomes, "form": form, "totals": totals, "active_tab": "ingresos",
    })


@login_required
@role_required("super_admin")
def income_edit(request, pk):
    income = get_object_or_404(Income, pk=pk)
    form = IncomeForm(request.POST or None, instance=income)
    if request.method == "POST" and form.is_valid():
        form.save()
        log_activity(request.user, "income_updated", {"income_id": income.id})
        messages.success(request, "Ingreso actualizado.")
        return redirect("finance:income_list")
    return render(request, "dashboard/income_form.html", {"form": form, "active_tab": "ingresos"})


@login_required
@role_required("super_admin")
def contract_list(request):
    if request.method == "POST":
        form = ContractForm(request.POST)
        if form.is_valid():
            contract = form.save()
            log_activity(request.user, "contract_created", {"contract_id": contract.id})
            messages.success(request, "Contratación registrada.")
            return redirect("finance:contract_list")
    else:
        form = ContractForm()

    contracts = Contract.objects.all()
    return render(request, "dashboard/contracts.html", {
        "contracts": contracts, "form": form, "active_tab": "contrataciones",
    })


@login_required
@role_required("super_admin")
def contract_edit(request, pk):
    contract = get_object_or_404(Contract, pk=pk)
    form = ContractForm(request.POST or None, instance=contract)
    if request.method == "POST" and form.is_valid():
        form.save()
        log_activity(request.user, "contract_updated", {"contract_id": contract.id})
        messages.success(request, "Contratación actualizada.")
        return redirect("finance:contract_list")
    return render(request, "dashboard/contract_form.html", {"form": form, "active_tab": "contrataciones"})
