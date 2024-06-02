import pexpect
child = pexpect.spawn('/bin/bash')
child.expect('$')
child.sendline('curl http://example.com/data.json')
child.sendline('\n')
child.expect('</html>')
with open('data.json', 'w') as f:
    f.write(child.before.decode(encoding='utf-8'))

child.sendline('exit')
child.expect(pexpect.EOF)

