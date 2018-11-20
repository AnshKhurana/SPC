import coreapi

auth = coreapi.auth.BasicAuthentication(username='pk', password='lokikoli', domain='127.0.0.1')
client = coreapi.Client(auth=auth)
document = client.get('http://'+'127.0.0.1:8000' + "/schema/")
print(document)
client.action(document, ['filedatabase', 'create'], params={'file_name':'machine-learning-ex8/ex8' \
    ,'file_type':'DIR','file_data':'10==','md5sum':'fkvmkf'})