from django.urls import reverse
from simple_kanban.tests.unit.base import BaseUnitTest
from simple_kanban.models import Project

class CreateProjectViewTest(BaseUnitTest):

  def test_create_project_post(self):
    url = reverse('project_create')
    
    #Construct a Project Form with SwimlaneFormSet data.
    data = {
        'name': 'New Project',
        'description': 'Testing Project',
        'form-TOTAL_FORMS': '1',
        'form-INITIAL_FORMS': '0',
        'form-MIN_NUM_FORMS': '0',
        'form-MAX_NUM_FORMS': '1000',
        'form-0-name': 'Swimlane 1',
        'form-0-sort_order': '1',
    }

    response = self.client.post(url, data)

    # Assertions
    self.assertRedirects(response, reverse('index'))
    self.assertEqual(Project.objects.count(), 2)
    self.assertEqual(Project.objects.last().name, 'New Project')
    self.assertEqual(Project.objects.last().swimlanes.count(), 1)
    self.assertEqual(Project.objects.last().swimlanes.last().name, 'Swimlane 1')
    self.assertEqual(Project.objects.last().swimlanes.last().sort_order, 1)

  def test_create_project_get(self):
    url = reverse('project_create')
    
    response = self.client.get(url)
    
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'kanban/project_form.html')