# pexpectライブラリからpxsshモジュールをインポート
from pexpect import pxssh
# timeモジュールをインポート
import time

# ログイン情報を設定しSSHサーバーにログイン
ssh = pxssh.pxssh()
ssh.login(server="127.0.0.1", #接続したいSSHサーバーのIPを記述
          username="devg1120", #SSHサーバー側のユーザー名を記述
          password="sakiko1120") #SSHサーバー側のユーザーのパスワードを記述
print(ssh.after.decode(encoding='utf-8'), flush=True) #出力結果1

# テキストファイル「test.txt」を作成する
ssh.sendline("touch test.txt")
ssh.expect(r"\[.*\]\$ ")
print(ssh.before.decode(encoding='utf-8'), flush=True) #出力結果2
print(ssh.after.decode(encoding='utf-8'), flush=True) #出力結果3
time.sleep(1)

# カレントディレクトリのファイルを表示する
ssh.sendline("ls -l")
ssh.expect(r"\[.*\]\$ ")
print(ssh.before.decode(encoding='utf-8'), flush=True) #出力結果4
print(ssh.after.decode(encoding='utf-8'), flush=True) #出力結果5
time.sleep(1)

# SSHサーバーからログアウト
ssh.logout()
