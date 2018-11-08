from pocket import Pocket
import os
import json

CONSUMER_KEY='81860-fe0e881dde885d9a16fb77aa'

# about:blank
# pocketapp1234:authorizationFinished
# javascript:window.close();
def get_access_token(consumer_key, redirect_uri="about:blank", auth_file = "~/.pocketauth"):
    auth_file = os.path.expanduser(auth_file)

    if os.path.isfile(auth_file):
        json_str = open(auth_file).read()
        config = json.loads(json_str)[0]

        if consumer_key in config:
            return config[consumer_key]
    else:
        config = [{}]

    request_token = Pocket.get_request_token(consumer_key=consumer_key, redirect_uri=redirect_uri)

    # URL to redirect user to, to authorize your app
    auth_url = Pocket.get_auth_url(code=request_token, redirect_uri=redirect_uri)
    input( 'Please open %s in your browser to authorize the app and '
        'press enter:' % auth_url
    )

    access_token = Pocket.get_access_token(consumer_key, request_token)
    print(access_token)
    # save access_token for later
    config[0][consumer_key] = access_token
    with open(auth_file, 'w+') as fp:
        json.dump(config, fp)

    secure_file(auth_file)
    return access_token

def secure_file(file):
    if os.name == 'nt':
        import win32security
        import ntsecuritycon as con
        import pdb
        userx, domain, type = win32security.LookupAccountName ("", "Everyone")
        sd = win32security.GetFileSecurity(file, win32security.DACL_SECURITY_INFORMATION)
        dacl = sd.GetSecurityDescriptorDacl()   # instead of dacl = win32security.ACL()
        dacl.AddAccessAllowedAce(win32security.ACL_REVISION, con.FILE_ALL_ACCESS, userx)
        sd.SetSecurityDescriptorDacl(1, dacl, 0)
        win32security.SetFileSecurity(file, win32security.DACL_SECURITY_INFORMATION, sd)
    else:
        os.chmod(file, 0o600)
