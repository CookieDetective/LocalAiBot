from python_postman import PythonPostman, Collection

#Lets thing about what this will need to do for regression tests
#Import Postman collections
#Import Postman environments
#Run postman collections with environments
"""
The arguments within a collection
        Args:
            info: Collection metadata
            items: List of items (requests and folders) in the collection
            variables: Optional list of collection-level variables
            auth: Optional collection-level authentication
            events: Optional list of collection-level events
"""

def import_collection(collection_path: str):
    """This function will import a single Postman collection"""
    collection = PythonPostman.from_file(collection_path)
    return collection

def import_environment(environment_path: str):
    """This function will import a single Postman environment"""
    environment = PythonPostman.from_file(environment_path)
    return environment

def find_request(request_name: str):
    """This function will find a request by name"""
    pass

def list_collection(collection: Collection,):
    """
    This function will list all items in a Postman collection
    Arg: collection (Collection): A Postman Collection object.
    Returns: List: A list of requests that are in the collection."""
    requests = []
    for item in collection.items:
        # If the item is a request
        if hasattr(item, "request"):
            requests.append(item)
        # If the item is a folder, iterate its items
        elif hasattr(item, "items"):
            for subitem in item.items:
                if hasattr(subitem, "request"):
                    requests.append(subitem)
    return requests

def list_tests_by_url(collection: Collection, url: str):
    """
    List all requests for a given Postman collection that match the specified URL.
    Args:
        collection (Collection): A Postman Collection object.
        url (str): The URL to filter requests by.
    Returns: List: A list of request items whose URL matches the 'url' parameter.
    """
    requests = list_collection(collection)
    matched_requests = [req for req in requests if str(req.request.url) in  url]
    return matched_requests