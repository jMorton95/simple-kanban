from typing import Union
from simple_kanban.utils.generic import form_is_valid, get_object_if_exists
from simple_kanban.forms.kanban.ticket_form import TicketForm
from simple_kanban.services.ticketcomment_service import TicketCommentService
from simple_kanban.models import Ticket

class TicketService():
  def DeleteSwimlaneTickets(request, swimlane):
    related_tickets = Ticket.objects.filter(ticket_swimlane=swimlane)
    for ticket in related_tickets:
      TicketCommentService.DeleteTicketComments(request, ticket)
      ticket.soft_delete(request.user)
      
  def GetCreateTicketContext(request, project_id):
    ticket_form = TicketForm(request, project_id)
    return {
      "ticket_form": ticket_form,
      "create_ticket": True
    }
  
  def CreateTicket(request, project_id):
    ticket_form = TicketForm(request, project_id, data=request.POST)
    
    if form_is_valid(request, ticket_form):
      ticket = ticket_form.save(commit=False)
      ticket.create(ticket.ticket_swimlane, request.user)
      return True
    else:
      return False
    
  def GetEditTicketContext(request, ticket):
    ticket_form = TicketForm(request, ticket.ticket_swimlane.swimlane_project.id, instance=ticket)
    return {
      "ticket_form": ticket_form,
      "ticket": ticket,
      "edit_ticket": True
    }
    
  def EditTicket(request, project_id, ticket):
    ticket_form = TicketForm(request, project_id, data=request.POST, instance=ticket)
    
    if form_is_valid(request, ticket_form):
      ticket = ticket_form.save(commit=False)
      ticket.update(request.user)
      return True
    else: 
      return False
    
  def GetTicketIfExists(request, ticket_id) -> Union[bool, Ticket | None]:
    return get_object_if_exists(request, Ticket, ticket_id)