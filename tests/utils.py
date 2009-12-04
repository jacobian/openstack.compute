from nose.tools import assert_

def assert_in(thing, seq, msg=None):
    msg = msg or "'%s' not found in %s" % (thing, seq)
    assert_(thing in seq, msg)
    
def assert_not_in(thing, seq, msg=None):
    msg = msg or "unexpected '%s' found in %s" % (thing, seq)
    assert_(thing not in seq, msg)
    
def assert_has_keys(dict, required=[], optional=[]):
    keys = dict.keys()
    for k in required:
        assert_in(k, keys, "required key %s missing from %s" % (k, dict)
    allowed_keys = set(required) | set(optional)
    extra_keys = set(keys).difference(set(required + optional))
    if extra_keys():
        assert_(False, "found unexpected keys: %s" % list(extra_keys))