# pexpectをimportする
import pexpect

# rootユーザーに切り替える
p = pexpect.spawn('env LANG=C su -')
p.expect("Password: ")
print(p.after.decode(encoding='utf-8')) 
p.sendline("sakiko1120")

p.expect("# ")
# 現在のディレクトリを確認する
p.sendline("pwd")
p.expect("# ")
print(p.before.decode(encoding='utf-8'))
print(p.after.decode(encoding='utf-8')) 


# 実行中のプロセスを一覧表示する
p.sendline("ps")
p.expect("# ")
print(p.before.decode(encoding='utf-8'))
