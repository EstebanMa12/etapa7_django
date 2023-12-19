import pytest


pytestmark = pytest.mark.django._db

class TestPostModel:
    def test_str_return(self,post_factory):
        post = post_factory(title='test-post')
        assert post._str_() == 'test-post'
        
        