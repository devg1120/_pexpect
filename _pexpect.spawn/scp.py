import pexpect
import sys

mypassword="sakiko1120"

#child = pexpect.spawn('scp /home/devg1120/_pexpect/_pexpect.spawn/foo devg1120@localhost:~/tmp')
child = pexpect.spawn('scp foo devg1120@localhost:~/tmp')
child.logfile = sys.stdout.buffer

child.expect('assword:')
child.sendline(mypassword)
#child.expect('$')
child.expect(pexpect.EOF)

