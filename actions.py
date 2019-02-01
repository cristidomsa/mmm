import csv
import time
import requests
import re

dictfilter = lambda x, y: dict([ (i,x[i]) for i in x if i in set(y) ])

class InstaActions:

    FIELDNAMES = ['username', 'pk']

    def __init__(self, session, user_account):
        self.insta = session
        self.user_account = user_account
        try:
            self.user_account_id = self._get_user_id(self.user_account)
        except Exception:
            print('User account does not exist!')
            self.user_account_id = None

    def _write_csv(self, filename, content):
        """Writes content to csv filename
        
        Arguments:
            filename {str} -- filename of the csv
            content {list} -- list of dictionaries to be written in csv
        """

        with open(filename, 'w') as myfile:
            wr = csv.DictWriter(myfile, fieldnames=self.FIELDNAMES)
            wr.writeheader()
            wr.writerows(content)   

    def _get_user_id(self, username):
        """Get user_id from Instagram
        
        Arguments:
            username {str} -- Name of the username to retrieve user_id

        Returns:
            int -- User_id from instagram
        """

        url = 'HTTPS://WWW.INSTAGRAM.COM/{}/?__A=1'.format(username)
        
        response = requests.get(url)
        p = re.compile(b'profilePage_(\d+)')
        return int(p.search(response.content).group(1))

    def _clean_data(self, user_list):
        """Function to filter information to be written in csv (based on FIELDNAMES)
        
        Arguments:
            user_list {list} -- User information list
        
        Returns:
            list -- Cleaned list of user information
        """

        result = []
        for u in user_list:
            result.append(dictfilter(u, self.FIELDNAMES))
        return result

    def get_following(self, user_id):
        """Get followings for user_id
        
        Arguments:
            user_id {int} -- User ID from Instagram
        
        Returns:
            list -- List of dictionaries containing cleaned users info
        """

        
        following   = []
        next_max_id = True
        while next_max_id:
            if next_max_id == True: next_max_id=''
            _ = self.insta.getUserFollowings(user_id,maxid=next_max_id)
            following.extend ( self.insta.LastJson.get('users',[]))
            next_max_id = self.insta.LastJson.get('next_max_id','')
            time.sleep(1) 
            
        return self._clean_data(following)
    
    def get_followers(self, user_id):
        """Get followers for user_id
        
        Arguments:
            user_id {int} -- User ID from Instagram
        
        Returns:
            list -- List of dictionaries containing cleaned users info
        """

        followers   = []
        next_max_id = True
        while next_max_id:
            if next_max_id == True: next_max_id=''
            _ = self.insta.getUserFollowers(user_id,maxid=next_max_id)
            followers.extend ( self.insta.LastJson.get('users',[]))
            next_max_id = self.insta.LastJson.get('next_max_id','')
            time.sleep(1) 
            
        return self._clean_data(followers)

    def do(self):
        """Executes the desired operations (from specs)
        """

        if self.user_account_id is not None:
            self._write_csv(self.user_account +'_followers.csv', self.get_followers(self.user_account_id))
        self._write_csv(self.insta.username +'_following.csv', self.get_following(self.insta.username_id))

        print('Files written!')

   