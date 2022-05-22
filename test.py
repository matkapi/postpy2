from postpy2.core import PostPython
import unittest2 as unittest
import json

pp = PostPython('collections/tests.postman_collection.json')
pp.environments.load('environments/test.postman_environment.json')

pp.environments.update({
    'server_url': 'https://httpbin.org'
})

# exit()
# pp.help()
response = pp.Folder.test1()
print(response.json())
print(response.status_code)
response = pp.Folder.test2()
print(response.json())
print(response.status_code)


response = pp.Folder.test_file()
print(response.status_code)
print(response.json())
pp.Folder.test_file.set_data([
    {
        "key": "title",
        "value": "bar"
    },
    {
        "key": "body",
        "value": "foo"}
])
pp.Folder.test_file.set_files([
    {
        "key": "two",
        "src": "aserts/2.png"
    }
])
response = pp.Folder.test_file()
print(response.status_code)
print(response.json())

pp.Folder.test2.set_json({"title": "bar", "body": "foo", "userId": 1})
response = pp.Folder.test2()
print(response.json())
print(response.status_code)

response = pp.Folder.graphql()
print(response.status_code)
print(len(response.json()))
