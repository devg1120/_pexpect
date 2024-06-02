import pexpect
import sys

mypassword="sakiko1120"

#child = pexpect.spawn('scp /home/devg1120/_pexpect/_pexpect.spawn/foo devg1120@localhost:~/tmp')
child = pexpect.spawn('scp test.sh devg1120@localhost:~/tmp')
child.logfile = sys.stdout.buffer

child.expect('assword:')
child.sendline(mypassword)
#child.expect('$')
child.expect(pexpect.EOF)

rsh = pexpect.spawn('ssh devg1120@localhost')
rsh.logfile = sys.stdout.buffer

rsh.expect('assword:')
rsh.sendline(mypassword)
rsh.expect('$')

rsh.sendline("stty rows 1000 cols 1000")
rsh.expect('$')
rsh.sendline("cat ~/tmp/test.sh")
rsh.expect('$')
rsh.sendline("bash ~/tmp/test.sh")

rsh.expect('$')
rsh.sendline("stty size")
rsh.expect('$')
rsh.sendline("logout")
rsh.expect(pexpect.EOF)
