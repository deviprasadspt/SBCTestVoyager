import pytest
from playwright.sync_api import sync_playwright

#verify the get comments request
def test_get_comments_success():
    with sync_playwright() as p:
        request = p.request.new_context()
        
        response = request.get('http://jsonplaceholder.typicode.com/comments')
        assert response.status == 200
        data = response.json()
        assert isinstance(data, list)
        for item in data:
            assert 'postId' in item
            assert 'id' in item
            assert 'name' in item
            assert 'email' in item
            assert 'body' in item

# verify the get comments request with parameters
@pytest.mark.parametrize("post_id", [1, 2, 3, 4, 5])
def test_get_comments_by_post_id(post_id):
    with sync_playwright() as p:
        request = p.request.new_context()
        
        response = request.get(f'http://jsonplaceholder.typicode.com/comments?postId={post_id}')
        data = response.json()
        assert isinstance(data, list)# check if the response is a list
        for item in data:
            assert item['postId'] == post_id
            assert 'id' in item
            assert 'name' in item
            assert 'email' in item
            assert 'body' in item