from django.shortcuts import render, redirect
from .models import Expenses
from django.contrib import messages


def data_table(request):
    """
    Fetches all expense records ordered by date (latest first) and passes them to the template.
    """
    data = Expenses.objects.order_by('-date').values()
    return render(request, 'index.html', {'data': list(data)})


def insert_data(request):
    """
    Handles expense data insertion based on user input (credit or debit transactions).
    """
    if request.method == "POST":
        description = request.POST.get('description', '').strip()
        action = request.POST.get('action', '').strip().lower()
        amount = request.POST.get('amount', '').strip()

        # Validate input
        if not description or not action or not amount.isdigit():
            messages.error(request, "Invalid input. Please provide valid details.")
            return redirect('insert_data')  # Redirect to the same page

        amount = int(amount)
        last_entry = Expenses.objects.order_by('-date').first()
        current_balance = last_entry.balance if last_entry else 0

        # Create new entry based on action type
        if action == 'credit':
            Expenses.objects.create(description=description, credits=amount, balance=current_balance + amount)
        elif action == 'debit':
            if amount > current_balance:
                messages.error(request, "Insufficient balance for this transaction.")
                return redirect('insert_data')
            Expenses.objects.create(description=description, debit=amount, balance=current_balance - amount)
        else:
            messages.error(request, "Invalid transaction type.")
            return redirect('insert_data')

        messages.success(request, "Transaction added successfully.")
        return redirect('data_table')  # Redirect to data table view

    return render(request, 'add_transaction_page.html')
