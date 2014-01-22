from django.contrib.sessions.backends.cache import SessionStore
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory
from nose.tools import assert_equal

from django.contrib.auth.models import User as AuthUser, AnonymousUser
from planbox_data.models import User, Project, Event
from planbox_ui.views import project_view, new_project_view, signup_view, signin_view


class PlanBoxUITestCase (TestCase):
    def setUp(self): self.set_up()
    def tearDown(self): self.tear_down()

    def set_up(self):
        self.factory = RequestFactory()

    def tear_down(self):
        AuthUser.objects.all().delete()
        User.objects.all().delete()
        Project.objects.all().delete()
        Event.objects.all().delete()


class SignupViewTests (PlanBoxUITestCase):
    def test_user_is_redirected_home_on_successful_signup(self):
        url = reverse('app-signup')

        user_data = {
            'username': 'mjumbewu',
            'password': '123',
            'email': 'mjumbewu@example.com',
            'affiliation': 'OpenPlans',
        }

        request = self.factory.post(url, data=user_data)
        request.user = AnonymousUser()
        request.session = SessionStore('session')
        response = signup_view(request)

        # If you get a 200 here, it's probably because of wrong form data.
        assert_equal(response.status_code, 302)
        assert_equal(response.url, reverse('app-new-project', kwargs={'owner_name': 'mjumbewu'}))

        user_profile = User.objects.get(auth__username='mjumbewu')
        assert_equal(user_profile.affiliation, 'OpenPlans')


class SigninViewTests (PlanBoxUITestCase):
    def test_user_is_redirected_home_on_successful_signin(self):
        AuthUser.objects.create_user(username='mjumbewu', password='123')
        url = reverse('app-signin')

        user_data = {
            'username': 'mjumbewu',
            'password': '123',
        }

        request = self.factory.post(url, data=user_data)
        request.user = AnonymousUser()
        request.session = SessionStore('session')
        response = signin_view(request)
        assert_equal(response.status_code, 302)
        assert_equal(response.url, reverse('app-new-project', kwargs={'owner_name': 'mjumbewu'}))


class NewProjectViewTests (PlanBoxUITestCase):
    def test_user_gets_redirected_to_own_new_project_page(self):
        auth1 = AuthUser.objects.create_user(username='mjumbewu', password='123')
        owner1 = auth1.profile
        project = Project.objects.create(slug='test-slug', title='test title', location='test location', description='test description', owner=owner1)

        auth2 = AuthUser.objects.create_user(username='atogle', password='456')

        url1_kwargs = {'owner_name': auth1.username}
        url1 = reverse('app-new-project', kwargs=url1_kwargs)
        url2_kwargs = {'owner_name': auth2.username}
        url2 = reverse('app-new-project', kwargs=url2_kwargs)

        request = self.factory.get(url1)
        request.user = auth2
        response = new_project_view(request, **url1_kwargs)
        assert_equal(response.status_code, 302)
        assert_equal(response.url, url2)

    def test_anon_user_gets_redirected_to_login(self):
        auth = AuthUser.objects.create_user(username='mjumbewu', password='123')

        url_kwargs = {'owner_name': auth.username}
        url = reverse('app-new-project', kwargs=url_kwargs)
        login_url = reverse('app-signin')

        request = self.factory.get(url)
        request.user = AnonymousUser()
        response = new_project_view(request, **url_kwargs)
        assert_equal(response.status_code, 302)
        assert_equal(response.url, login_url + '?next=' + url)

    def test_user_gets_redirected_to_existing_project(self):
        # NOTE: This test is only relevant as long as users can have only one
        #       project.
        auth = AuthUser.objects.create_user(username='mjumbewu', password='123')
        owner = auth.profile
        project = Project.objects.create(slug='test-slug', title='test title', location='test location', description='test description', owner=owner)

        url_kwargs = {'owner_name': auth.username}
        url = reverse('app-new-project', kwargs=url_kwargs)
        project_url_kwargs = {'owner_name': auth.username, 'slug': project.slug}
        project_url = reverse('app-project', kwargs=project_url_kwargs)

        request = self.factory.get(url)
        request.user = auth
        response = new_project_view(request, **url_kwargs)
        assert_equal(response.status_code, 302)
        assert_equal(response.url, project_url)


class ProjectDetailViewTests (PlanBoxUITestCase):
    def test_anon_gets_non_editable_details(self):
        auth = AuthUser.objects.create_user(username='mjumbewu', password='123')
        owner = auth.profile
        project = Project.objects.create(slug='test-slug', title='test title', location='test location', description='test description', owner=owner)

        kwargs = {
            'owner_name': 'mjumbewu',
            'slug': 'test-slug'
        }

        url = reverse('app-project', kwargs=kwargs)
        request = self.factory.get(url)
        request.user = AnonymousUser()
        response = project_view(request, **kwargs)

        assert_equal(response.status_code, 200)
        assert_equal(response.context_data.get('is_owner'), False)

    def test_non_planbox_user_gets_non_editable_details(self):
        auth = AuthUser.objects.create_user(username='mjumbewu', password='123')
        owner = auth.profile
        project = Project.objects.create(slug='test-slug', title='test title', location='test location', description='test description', owner=owner)

        kwargs = {
            'owner_name': 'mjumbewu',
            'slug': 'test-slug'
        }

        auth2 = AuthUser.objects.create_user(username='atogle', password='456')

        url = reverse('app-project', kwargs=kwargs)
        request = self.factory.get(url)
        request.user = auth2
        response = project_view(request, **kwargs)

        assert_equal(response.status_code, 200)
        assert_equal(response.context_data.get('is_owner'), False)

    def test_non_owner_gets_non_editable_details(self):
        auth = AuthUser.objects.create_user(username='mjumbewu', password='123')
        owner = auth.profile
        project = Project.objects.create(slug='test-slug', title='test title', location='test location', description='test description', owner=owner)

        kwargs = {
            'owner_name': 'mjumbewu',
            'slug': 'test-slug'
        }

        auth2 = AuthUser.objects.create_user(username='atogle', password='456')
        owner2 = auth2.profile

        url = reverse('app-project', kwargs=kwargs)
        request = self.factory.get(url)
        request.user = auth2
        response = project_view(request, **kwargs)

        assert_equal(response.status_code, 200)
        assert_equal(response.context_data.get('is_owner'), False)

    def test_owner_gets_editable_details(self):
        auth = AuthUser.objects.create_user(username='mjumbewu', password='123')
        owner = auth.profile
        project = Project.objects.create(slug='test-slug', title='test title', location='test location', description='test description', owner=owner)

        kwargs = {
            'owner_name': 'mjumbewu',
            'slug': 'test-slug'
        }

        url = reverse('app-project', kwargs=kwargs)
        request = self.factory.get(url)
        request.user = auth
        response = project_view(request, **kwargs)

        assert_equal(response.status_code, 200)
        assert_equal(response.context_data.get('is_owner'), True)

