import json
import os
from pathlib import Path 
import pytest
from playwright.sync_api import sync_playwright

# Helper function to determine current_directory, project_root, and url_file_path
def load_endpoints_from_json(endpoint):
    # Determine the current directory and project root
    current_directory = os.path.dirname(os.path.abspath(__file__)) 

    # Traverse up the directory tree to fnd the 'SBTESTVOYAGER' directory
    project_root_dir = current_directory
    while os.path.basename(project_root_dir) != 'SBCTestVoyager':
        project_root_dir = os.path.dirname(project_root_dir)

        # Reached the filesystem root
        if project_root_dir == os.path.dirname(project_root_dir):
            raise FileNotFoundError("The project root directory 'SBTESTVOYAGER' was not found.")

    # Construct the path to the 'data' and 'endpoints.json' file
    data_folder = os.path.join(project_root_dir, 'data')
    endpoints_file = os.path.join(data_folder, 'endpoints.json')    
    
    # Load the base api from JSON file
    with open(endpoints_file, 'r') as file:
        data = json.load(file)
        base_url = data["sb_cloud_api_base"] # Debug print statement

      
    # Construct the full URL
    full_url = f"{base_url}/{endpoint}"
    #print(f"Debug: Constructed full_url: {full_url}") # Debug print statement
    #print(f"\nfull_url: {full_url}") # Debug print statement
    return full_url

def make_get_request(endpoint):
    sb_api = load_endpoints_from_json(endpoint)
    with sync_playwright() as p:
        request = p.request.new_context()
        response = request.get(sb_api)
        json_data = response.json()
        return response, json_data

# *** Test Cases: N *** try to update the N in this value dynamically#

# Verify response status
def test_get_posts_success():

    response,json_data = make_get_request('posts/1')
    assert response.status == 200

# Verify response headers
def test_get_response_headers():
    response,json_data = make_get_request('posts/1')
    
    # Expected headers
    expected_headers = {'content-type': 'application/json; charset=utf-8'}

    # Normalize the headers to lowercase
    response_headers = {key.lower(): value for key, 
                        value in response.headers.items()}
    
    # Compare the expected headers to the actual headers
    for key, value in expected_headers.items():
        assert response_headers.get(key) == value    

# Verify response for list of items
def test_get_response_lists():
    response,json_data = make_get_request('posts')
    assert isinstance(json_data, list)
    assert len(json_data) > 0

# Verify response for attributes
def test_get_response_attributes():
    # Use the helper function to load the endpoints
    response, json_data = make_get_request('posts/1')
    
    expected_attributes = ['userId', 'id', 'title', 'body']
    json_data = [json_data] # Convert the json_data to a list

    for attribute in expected_attributes:
        assert attribute in json_data[0]