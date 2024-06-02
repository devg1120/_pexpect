import pexpect

child = pexpect.spawn('/bin/bash')
child.expect('$')
child.sendline('pwd')
child.expect('$')
print(child.before.decode(encoding='utf-8'))
print(child.after.decode(encoding='utf-8'))

