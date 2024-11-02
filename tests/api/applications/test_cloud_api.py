import json
import os
from pathlib import Path 
import pytest
from playwright.sync_api import sync_playwright

# Helper function to determine current_directory, project_root, and url_file_path
def load_endpoints_from_json(endpoint):
    # Determine the current directory and project root
    current_directory = Path.cwd()
    project_root = current_directory.parents[2] # go up 2 levels to the project root
    url_file_path = project_root / 'data' / 'endpoints.json'

    # Check if the file exists
    if not url_file_path.is_file():
        raise FileNotFoundError(f"The file {url_file_path} does not exist.")
    
    # Load the base api from JSON file
    with open(url_file_path, 'r') as file:
        data = json.load(file)
        base_url = data['sb_cloud_api_base']
        # print(f"\nbase_url: {base_url}") # Debug print statement
        
    # Construct the full URL
    full_url = f"{base_url}/{endpoint}"
    #print(f"Debug: Constructed full_url: {full_url}") # Debug print statement
    #print(f"\nfull_url: {full_url}") # Debug print statement
    return full_url

    
def test__get_posts_success():
    # Use the helper function to load the endpoints
    sb_api = load_endpoints_from_json('posts/1')

    # print(f"\n sb_api: {sb_api}") # Debug print statement
    
    with sync_playwright() as p:
        request = p.request.new_context()
        
        response = request.get(sb_api)
        assert response.status == 200
        
        
# @pytest.mark.skip(reason="Skipping this test for now")
def test_list_of_attributes():
    # Use the helper function to load the endpoints
    sb_api = load_endpoints_from_json('posts/1')

    with sync_playwright() as p:
        request = p.request.new_context()
        response = request.get(sb_api)
        data = response.json()
        #Check if the response is a dictionary
        assert isinstance(data, dict)
        #Check if the required keys are present in the dictionary
        for item in data:
            assert 'userId' in data
            assert  'id' in data