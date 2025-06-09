from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from accounts.models import User
from task_manager.models import Project, Task
from task_manager.models.task import StatusChoice
from rest_framework.test import APITestCase






class ProjectTaskModelTest(TestCase):

    def setUp(self):
        self.owner = User.objects.create_user(username='ikromjon',password='1996')
        self.member = User.objects.create_user(username='islomjon',password='2000')

        self.project = Project.objects.create(
            name = 'test',
            description = 'test qilish',
            owner = self.owner
        )
        self.project.members.add(self.member)


        self.task = Task.objects.create(
            title='test qilish',
            project=self.project,
            user=self.member,
            status=StatusChoice.PROCESS
        )

    def test_project_created(self):
        self.assertEqual(Project.objects.count(),1)
        self.assertEqual(self.project.name,'test')
        self.assertIn(self.member,self.project.members.all())


    def test_task_created(self):
        self.assertEqual(Task.objects.count(),1)
        self.assertEqual(self.task.status,StatusChoice.PROCESS)
        self.assertEqual(self.task.title,'test qilish')




    class ProjectIntegrationTest(APITestCase):
        def setUp(self):
            self.owner =  User.objects.create_user(username='Abdulla',password='1997')
            self.member = User.objects.create_user(username='Doston',password='1997')

            self.client.login(username='Abdulla',password='1997')

            self.project_url = reverse('project')
            self.task_url = reverse('task')

            self.project_data = {
                'name':'Test project',
                'description':'test qilish',
                'owner':self.owner.pk,
                'members':[self.member.pk]
            }

            self.task_data = {
                'title':'test yaratish',
                'project': None,
                'user': None,
                'status': StatusChoice.PROCESS.value
            }

        def test_creeate_project_and_task(self):
            project_response = self.client.post(self.project_url,self.project_data,format='json')
            self.assertEqual(project_response.status_code,status.HTTP_201_CREATED)
            self.assertEqual(Project.objects.count(),1)

            project_id = project_response.data['id']

            project_members = project_response.data['members']

            self.task_data['project']=project_id
            self.task_data['user']=project_members[0]['id']

            response = self.client.post(self.task_url,self.task_data,format='json')
            self.assertEqual(response.status_code,status.HTTP_201_CREATED)
            self.assertEqual(Task.objects.count(),1)

            task = Task.objects.first()
            self.assertEqual(task.title,self.task_data['title'])
            self.assertEqual(task.project.id,self.task_data['project'])
            self.assertEqual(task.status,self.task_data['status'])
            self.assertEqual(task.user.id,self.task_data['user'])



