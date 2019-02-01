from InstagramAPI import InstagramAPI
from actions import InstaActions

def read_auth():
    """Reads user authentification credentials from keyboard
    
    Returns:
        username (str) -- Username
        password (str) -- Password
    """
    print('> Please provide your username and password:')
    username = input('< ')
    password = input('< ')
    return username, password


def read_user_account():
    """Reads user account from keyboard
    
    Returns:
        user_account (str) -- User account name
    """
    
    print('> Logged successfully! Please provide the user account name:')
    user_account = input('< ')
    return user_account

def login(username, password):
    """Login Instagram API object
    
    Arguments:
        username {str} -- Username
        password {str} -- Password
    
    Returns:
        InstagramAPI object -- Returns a InstagramAPI session object
    """

    insta = InstagramAPI(username, password)
    insta.login()
    return insta

if __name__ == '__main__':

    logged = False
    exists = False
    while not logged:
        u, p = read_auth()
        sess = login(u,p)
        if sess.isLoggedIn:
            logged = True
            usr = read_user_account()
            insta = InstaActions(sess, usr)
            insta.do()
        else:
            print('Login Failed! Try again.')



