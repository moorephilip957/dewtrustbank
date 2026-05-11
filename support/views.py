from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import TicketForm
from .models import Ticket, TicketMessage
from kyc.decorator import kyc_required

@login_required
# @kyc_required
def create_ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)

        if form.is_valid():
            ticket = form.save(commit=False)

            # attach logged-in user if available
            if request.user.is_authenticated:
                ticket.user = request.user
                ticket.name = request.user.first_name
                ticket.email = request.user.email
            else:
                ticket.name = request.POST.get("name")
                ticket.email = request.POST.get("email")

            ticket.save()

            # Create the initial message in TicketMessage
            TicketMessage.objects.create(
                ticket=ticket,
                sender="user",
                content=ticket.message,
                # attachment=ticket.attachment  # optional
            )

            messages.success(
                request,
                f"Ticket submitted successfully. Your reference ID is {ticket.reference_id}"
            )

            return redirect("customer:ticket_success", reference_id=ticket.reference_id)

        messages.error(request, "Please correct the errors below.")

    else:
        form = TicketForm()

    return render(request, "support/create_ticket.html", {"form": form})


@login_required
# @kyc_required
def ticket_success(request, reference_id):
    ticket = get_object_or_404(Ticket, reference_id=reference_id)
    return render(request, "support/ticket_success.html", {"ticket": ticket})


@login_required
# @kyc_required
def ticket_list(request):
    tickets = Ticket.objects.filter(user=request.user).order_by("-updated_at")

    status = request.GET.get("status")

    if status and status != "all":
        tickets = tickets.filter(status=status)

    return render(request, "support/ticket_list.html", {
        "tickets": tickets
    })


@login_required
# @kyc_required
def ticket_detail(request, reference_id):
    # Fetch ticket only for the logged-in user
    ticket = get_object_or_404(Ticket, reference_id=reference_id, user=request.user)
    
    # Fetch all messages related to this ticket, ordered chronologically
    messages_qs = ticket.messages.all().order_by("created_at")
    
    if request.method == "POST":
        content = request.POST.get("message")
        attachment = request.FILES.get("attachment")

        if content or attachment:
            # Save the new message
            TicketMessage.objects.create(
                ticket=ticket,
                sender="user",
                content=content,
                attachment=attachment
            )

            # Optionally update ticket timestamp or status
            ticket.status = "in_progress"
            ticket.save()

            messages.success(request, "Your message has been sent.")
            return redirect("support:ticket_detail", reference_id=ticket.reference_id)
        else:
            messages.error(request, "Please enter a message or attach a file.")

    return render(request, "support/ticket_detail.html", {
        "ticket": ticket,
        "messages": messages_qs
    })