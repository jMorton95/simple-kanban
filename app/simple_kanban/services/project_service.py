from typing import Union
from django.db.models import Prefetch
from simple_kanban.utils.auth import CreateUserContext
from simple_kanban.models import Project, Swimlane, Ticket, TicketComment
from simple_kanban.forms.kanban.project_form import ProjectForm
from simple_kanban.forms.kanban.swimlane_form import SwimlaneFormSet
from simple_kanban.utils.generic import form_is_valid, get_object_if_exists

class ProjectService():

  def GetProjectFormContext(request, is_update: bool, project: Project | None = None):
    project_form = ProjectForm(instance=project)
    swimlane_formset = SwimlaneFormSet(
      queryset=Swimlane.objects.filter(swimlane_project=project) if project 
      else Swimlane.objects.none())
    
    return CreateUserContext(request, {
        "project_form": project_form,
        "swimlane_formset": swimlane_formset,
        "is_update": is_update,
        "project": project
    })
  
  def GetProjectContext(request, project: Project):
    project_data = Project.objects.prefetch_related(
        Prefetch('swimlane_set', queryset=Swimlane.objects.prefetch_related(
            Prefetch('ticket_set', queryset=Ticket.objects.prefetch_related(
                'assignee', 'reporter',
                Prefetch('ticketcomment_set', queryset=TicketComment.objects.select_related('user')
            ))
        ))
    )).filter(id=project.id).first()
    
    return CreateUserContext(request, {
        'project': project_data,
        'swimlanes': project_data.swimlane_set.all(),
    })
  
  def CreateProject(request) -> bool:
    project_form = ProjectForm(request.POST)
    swimlane_formset = SwimlaneFormSet(request.POST)
    
    if form_is_valid(request, project_form) and form_is_valid(request, swimlane_formset):
      project = project_form.save(commit=False)
      project.create(request.user)

      for swimlane_form in swimlane_formset:
          if swimlane_form.cleaned_data:
              (swimlane_form
                .save(commit=False)
                .create(project, request.user))
      return True
    else: 
      return False
    
  def EditProject(request, project) -> bool:
    project_form = ProjectForm(request.POST, instance=project)
    swimlane_formset = SwimlaneFormSet(request.POST, queryset=Swimlane.objects.filter(swimlane_project=project))
    
    if form_is_valid(request, project_form) and form_is_valid(request, swimlane_formset):
      project = project_form.save(commit=False)
      project.update(request.user)
      
      for swimlane_form in swimlane_formset:
        if swimlane_form.cleaned_data:
          swimlane = swimlane_form.save(commit=False)
          swimlane.swimlane_project = project
          swimlane.update(request.user)
      return True
    else: 
      return False
  
  def GetProjectIfExists(request, project_id) -> Union[bool, Project | None]:
    return get_object_if_exists(request, Project, project_id)
  
