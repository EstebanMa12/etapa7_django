import pytest


pytestmark = pytest.mark.django_db

class TestPostModel:
    @pytest.mark.django_db
    def test_str_return(self, post_factory):
        post = post_factory(title='test-post')
        assert post.__str__() == 'test-post'
    
    @pytest.mark.django_db
    def test_post_model(self, post_factory, user_factory):
        user = user_factory(username = 'test-user')
        post = post_factory(title='test-post',
                            content='test-content',
                            author=user,
                            read_permission='public',
                            edit_permission='public')
        assert post.title == 'test-post'
        assert post.content == 'test-content'
        assert post.author.username == 'test-user'
        assert post.read_permission == 'public'
        assert post.edit_permission == 'public'
        
    @pytest.mark.django_db
    def test_post_model_title_length(self, post_factory, user_factory):
        user = user_factory(username = 'test-user')
        post = post_factory(title='t'*100,
                            content='test-content',
                            author=user)
        assert len(post.title) <= 100
        
    @pytest.mark.django_db
    def test_post_model_content_length(self, post_factory, user_factory):
        user = user_factory(username = 'test-user')
        post = post_factory(title='test-post',
                            content='t'*1000,
                            author=user)
        assert len(post.content) <= 1000
        
    @pytest.mark.django_db
    def test_post_model_read_permission(self, post_factory, user_factory):
        user = user_factory(username = 'test-user')
        post = post_factory(title='test-post',
                            content='test-content',
                            author=user,
                            read_permission='public')
        assert post.read_permission == 'public'
        
    @pytest.mark.django_db
    def test_post_model_edit_permission(self, post_factory, user_factory):
        user = user_factory(username = 'test-user')
        post = post_factory(title='test-post',
                            content='test-content',
                            author=user,
                            edit_permission='public')
        assert post.edit_permission == 'public'
        
    @pytest.mark.django_db
    def test_post_model_read_permission_choices(self, post_factory, user_factory):
        user = user_factory(username = 'test-user')
        post = post_factory(title='test-post',
                            content='test-content',
                            author=user,
                            )
        assert post.read_permission in ['public', 'authenticated', 'team', 'author']
        assert post.edit_permission in ['public', 'authenticated', 'team', 'author']
        
    @pytest.mark.django_db
    def test_post_model_created_at(self, post_factory, user_factory):
        user = user_factory(username = 'test-user')
        post = post_factory(title='test-post',
                            content='test-content',
                            author=user)
        assert post.created_at
        
    @pytest.mark.django_db
    def test_post_model_permissions(self, post_factory, user_factory):
        user = user_factory(username = 'test-user')
        post = post_factory(title='test-post',
                            content='test-content',
                            author=user,
                            read_permission='authenticated',
                            edit_permission='team')
        assert post.read_permission == 'authenticated'
        assert post.edit_permission == 'team'
    
    @pytest.mark.django_db
    def test_post_model_ordering(self, post_factory, user_factory):
        user = user_factory(username = 'test-user')
        post = post_factory(title='test-post',
                            content='test-content',
                            author=user,
                            read_permission='public',
                            edit_permission='public')
        assert str(post._meta.ordering) == "['-created_at']"