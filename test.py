from postpy2.core import PostPython

pp = PostPython('collections/tests.postman_collection.json')
pp.environments.load('environments/test.postman_environment.json')

pp.environments.update({
    'server_url': 'https://jsonplaceholder.typicode.com'
})

# pp.help()
response = pp.Folder.test1()
print(response.json())
print(response.status_code)
response = pp.Folder.test2()
print(response.json())
print(response.status_code)
