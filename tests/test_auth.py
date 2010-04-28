import mock
import cloudservers
import httplib2
from nose.tools import assert_raises, assert_equal

def test_authenticate_success():
    cs = cloudservers.CloudServers("username", "apikey")
    auth_response = httplib2.Response({
        'status': 204,
        'x-server-management-url': 'https://servers.api.rackspacecloud.com/v1.0/443470',
        'x-auth-token': '1b751d74-de0c-46ae-84f0-915744b582d1',
    })
    mock_request = mock.Mock(return_value=(auth_response, None))
    with mock.patch_object(httplib2.Http, "request", mock_request):
        cs.client.authenticate()
        mock_request.assert_called_with(cs.client.AUTH_URL, 'GET', 
            headers = {
                'X-Auth-User': 'username',
                'X-Auth-Key': 'apikey',
                'User-Agent': cs.client.USER_AGENT
            })
        assert_equal(cs.client.management_url, auth_response['x-server-management-url'])
        assert_equal(cs.client.auth_token, auth_response['x-auth-token'])

def test_authenticate_failure():
    cs = cloudservers.CloudServers("username", "apikey")
    auth_response = httplib2.Response({'status': 401})
    mock_request = mock.Mock(return_value=(auth_response, None))
    with mock.patch_object(httplib2.Http, "request", mock_request):
        assert_raises(cloudservers.Unauthorized, cs.client.authenticate)
        
def test_auth_automatic():
    client = cloudservers.CloudServers("username", "apikey").client
    client.management_url = ''
    mock_request = mock.Mock(return_value=(None, None))
    with mock.patch_object(client, 'request', mock_request):
        with mock.patch_object(client, 'authenticate') as mock_authenticate:
            client.get('/')
            mock_authenticate.assert_called()
            mock_request.assert_called()
            
def test_auth_manual():
    cs = cloudservers.CloudServers("username", "password")
    with mock.patch_object(cs.client, 'authenticate') as mocked:
        cs.authenticate()
        mocked.assert_called()