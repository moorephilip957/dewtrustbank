from django.shortcuts import render

from .forms import LocalTransferForm

def local_transfer(request):
    form = LocalTransferForm(request.POST, user=request.user)

    context = {
        'form': form,
    }
    return render(request, 'transactions/local_transfer.html', context)
