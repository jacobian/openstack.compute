import mock
import httplib2
from nose.tools import assert_raises, assert_equal
from openstack import compute

def test_authenticate_success():
    cs = compute.Compute(username="username", apikey="apikey")
    auth_response = httplib2.Response({
        'status': 204,
        'x-server-management-url': 'https://servers.api.rackspacecloud.com/v1.0/443470',
        'x-auth-token': '1b751d74-de0c-46ae-84f0-915744b582d1',
    })
    mock_request = mock.Mock(return_value=(auth_response, None))
    
    @mock.patch.object(httplib2.Http, "request", mock_request)
    def test_auth_call():
        cs.client.authenticate()
        mock_request.assert_called_with(cs.config.auth_url, 'GET', 
            headers = {
                'X-Auth-User': 'username',
                'X-Auth-Key': 'apikey',
                'User-Agent': cs.config.user_agent
            })
        assert_equal(cs.client.management_url, auth_response['x-server-management-url'])
        assert_equal(cs.client.auth_token, auth_response['x-auth-token'])

    test_auth_call()

def test_authenticate_failure():
    cs = compute.Compute(username="username", apikey="apikey")
    auth_response = httplib2.Response({'status': 401})
    mock_request = mock.Mock(return_value=(auth_response, None))
    
    @mock.patch.object(httplib2.Http, "request", mock_request)
    def test_auth_call():
        assert_raises(compute.Unauthorized, cs.client.authenticate)
        
    test_auth_call()
        
def test_auth_automatic():
    client = compute.Compute(username="username", apikey="apikey").client
    client.management_url = ''
    mock_request = mock.Mock(return_value=(None, None))
    
    @mock.patch.object(client, 'request', mock_request)
    @mock.patch.object(client, 'authenticate')
    def test_auth_call(m):
        client.get('/')
        m.assert_called()
        mock_request.assert_called()
    
    test_auth_call()
    
def test_auth_manual():
    cs = compute.Compute(username="username", apikey="apikey")
    
    @mock.patch.object(cs.client, 'authenticate')
    def test_auth_call(m):
        cs.authenticate()
        m.assert_called()

    test_auth_call()