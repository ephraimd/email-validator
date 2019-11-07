import os.path
import os
import sys 
from threading import Thread
from random import randint
import time
from dns.resolver import query
import socket
import smtplib
import json
from email_validator import *
from netScratcher import badKitten

api_url = 'http://api.apility.net/bademail/'
clean_output_file = 'clean-email-list.txt'
bad_output_file = 'bad-email-list.txt'
blaklist_output_file = 'blacklisted-email-list.txt'
role_output_file = 'role-email-list.txt'
proxy_reload = 100;
system_delay = 10 #seconds
sys_delay_interval = proxy_reload #at every 100th connections
proxyMan = badKitten(system_delay);


class workerThread:#(Thread):
    def __init__(self, email, line, fname):
        #Thread.__init__(self)
        self.email = email
        self.line = line
        self.fname = fname
        self.run()
        
    def run(self):
        print('Processing email {0} on line {1}'.format(self.email, self.line))
        self.initFIO()
        if self.line % proxy_reload == 0:
            time.sleep(system_delay)
            proxyMan.loadProxies() #reload new proxies please
            print('\t reloading proxy List!!')
        self.logEmail(self.processEmail(self.email))
        #time.sleep(randint(1, 5))
        pass

    def processEmail(self, email):
        try:
            v = validate_email(email.rstrip("\r\n")) # validate and get info
            email = v["email"] # replace with normalized form
            self.mxrecord = self.getMXRecord(email.split('@')[1])
            if self.mxrecord == False:
                print('\t Email Server non existent!!')
                return 'bad'
            print('\t Detected MX Server: %s \n' % self.mxrecord)
            print('\t Now Attempting to detect bad reputation!')
            response = proxyMan.scratchAPI(api_url, self.email)
            if response == False:
                print('\t API not accessible, will fall back to native methods!')
            else:
                data = response
                if len(data['response']['email']['blacklist']) != 0 or len(data['response']['ip']['blacklist']) != 0 or len(data['response']['domain']['blacklist']) != 0 or len(data['response']['domain']['blacklist_ns']) != 0:
                    print('\t API detected blacklisted email!')
                    return 'blacklist'
                elif data['response']['smtp']['exist_address'] == False:
                    print('\t API detected non-user email!')
                    return 'bad'
                elif data['response']['address']['is_role'] == True:
                    print('\t API detected role based email!')
                    return 'role'
                else:
                    print('\t Email is deliverable!')
                    return 'good'
                pass
            #we only come here if online API fails, this is the part where
            #IP will get blacklisted possibly
            print('\t Pausing before SMTP querying!')
            time.sleep(system_delay/3)
            print('\t Now Performing SMTP querying!')
            ret = self.checkEmailUser()
            if ret is False:
                print('\t Email User Account is not deliverable!')
                return False
            elif ret is None:
                print('\t Failed to perform smtp query!\n')
                #accounts like this are 70% valid
            print('\t Done hEre!')
            return True
        except EmailNotValidError as e:
            # email is not valid, exception message is human-readable
            print('\t %s' % str(e))
            return False
        pass

    def checkFirstLevel(self):
        pass

    def isEmailBlacklisted(self):
        pass

    def checkEmailUser(self):
        try:
            # Get local server hostname
            host = socket.gethostname()
            # SMTP lib setup (use debug level for full output)
            server = smtplib.SMTP()
            server.set_debuglevel(0)
            # SMTP Conversation
            server.connect(self.mxrecord)
            server.helo(host)
            server.mail('me@domain.com')
            code, message = server.rcpt(str(self.email))
            server.quit()
            # Assume 250 as Success
            if code == 250:
                return True
            else:
                return False
        except:
            return None
        pass

    def checkServerIsCatchAll(self):
        pass

    def getMXRecord(self,smtpserver):
        try:
            record = str(query(smtpserver, 'MX')[0].exchange)
            return record
        except:
            print('Failed to retreive MX Record service for %s' % smtpserver)
            return False

    def initFIO(self):
        self.good_fh = open(clean_output_file, 'a')
        self.bad_fh = open(bad_output_file, 'a')
        self.blk_fh = open(blaklist_output_file, 'a')
        self.role_fh = open(role_output_file, 'a')
        
    def logEmail(self, email_type):
        if email_type == 'good':
            self.good_fh.write(self.email)
            print('\t Email is good! Logged to %s' % clean_output_file)
        elif email_type == 'blacklist':
            self.blk_fh.write(self.email)
        elif email_type == 'role':
            self.role_fh.write(self.email)
        else:
            self.bad_fh.write(self.email)

    def closeIO(self):
        self.good_fh.close()
        self.bad_fh.close()
        self.blk_fh.close()
        self.role_fh.close()
    
class EmailValidator:

    def __init__(self, file=None):
        try:
            if file is not None:
                self.loadList(file)
                return
            if os.path.exists('email_chunks') is False:
                os.mkdir('email_chunks')
            process_list = []
            fileCount = -1
            with os.scandir('email_chunks') as iterator:
                for node in iterator:
                    if node.name.endswith('.txt'):
                        print('Started Processing %s' % node.name)
                        self.loadList('email_chunks/'+node.name)
                        os.system('cls')
                        print('Done with %s\n' % node.name)
            #self.loadList(input('Enter text file containing the list___ '))
            #self.loadList('email_list.txt')
            #self.shutdown()
        except OSError as err:
            print('IO Error: %s' % err)

    def loadList(self, filename):
        self.threads = []
        with open(filename) as fh:
            for line, email in enumerate(fh):
                workerThread(email, line, filename)
                
        pass

    def shutdown(self):
        if len(self.threads) != 0:
            for thread in self.threads:
                thread.start()
            for thread in self.threads:
                thread.join()

