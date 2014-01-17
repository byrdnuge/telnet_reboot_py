__author__ = 'jbergoon'

import telnetlib
import re
from socket import error


class DeviceActions:
    credentials = {
        'username': 'password',
		'username2': 'password2'
        
        '': ''
    }

    def reboot_iad(self, address):
        try:
            tn = telnetlib.Telnet(address)
        except:
            print "Cannot connect to iad {} Exception thrown".format(address)
            return
        for username, password in self.credentials.iteritems():
           # print "username: {} password: {}".format(username, password)
            tn.read_until('Username:')
            tn.write('{}\r'.format(username))
            tn.write('{}\r'.format(password))
            resp = tn.read_until('% Login Failure.', timeout=1).strip()
            regex = re.compile("^.*#$",re.MULTILINE)
            r = regex.search(resp)
            print 'response is {}'.format(resp)
            if resp == '% Login invalid':
                print "login failed"
                continue
            elif r:
                print "resp: {}".format(resp)
                print "login success"
                tn.write('write memory\r')
                print tn.read_until('[OK]')
                tn.write('reload\r')
                print tn.read_until('[confirm]')
                print tn.write('\r')
                tn.close()
                break
            #elif error is not None:
            #    print error
            #    return
            else:
                 print  "Failed to complete task on IAD at {}".format(address)
                 return

    def reboot_adit1(self, address):
            tn = telnetlib.Telnet(address)
            tn.read_until('Login:')
            tn.write('username\r')
            tn.read_until(':')
            tn.write('password\r')
            tn.read_until('>', timeout=4)
            tn.write('reset\ry')
            tn.close()
            print 'Completed reboot of {}'.format(address)

    def reboot_adit2(self, address):
            tn = telnetlib.Telnet(address)
            tn.read_until('Login:')
            tn.write('username1\r')
            tn.read_until(':')
            tn.write('password1\r')
            tn.read_until('>', timeout=4)
            tn.write('reset\ry')
            tn.close()
            print 'Completed reboot of {}'.format(address)



rooters = {
    "adit1": [
        "address",
    ],
    "adit2": [
        "address"    ]
	"iad":   [
		"address"
	]
}

action = DeviceActions()
for address in rooters['adit1']:
    print "Rebooting Adit at {} username username1".format(address)
    action.reboot_adit1(address)

for address in rooters['adit2']:
    print "Rebooting Adit at {} username username2".format(address)
    action.reboot_adit1(address)

for address in rooters['iad']:
    print "Rebooting IAD at {}".format(address)
    action.reboot_iad(address)




