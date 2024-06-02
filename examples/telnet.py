import pexpect # 同じディレクトリに置いたらこれだけで使える。

c = pexpect.spawn("telnet 192.168.0.2")
# spawnした時点から、pexpectは入力に対する出力(=stdout?)の内容を内部的に保持する。

c.expect("login: ")
# expectした時点で、内部的に保持するstdoutをspawn.bufferに読み込み、
# 与えられた正規表現で検索を行い、結果を以下の変数に出力する。
# spawn.after - マッチした文字列
# spawn.before - マッチした文字列より前の文字列
# spawn.buffer - マッチした文字列より後の文字列

# つまり、上の例で言えば結果は
print c.after # "login: "
print c.before # "Trying 192.168.0.2...\r\nConnected to 192.168.0.2.\r\nEscape character is '^}'.\r\n"
print c.buffer # ""
# となる。

c.sendline("spam")
c.expect("Password: ")
c.sendline("hamegg")
c.expect("spam@blackknight:\/export\/home\/spam\([0-9]+\)> $")

# ログインも終わった所でexpectとbufferと内部保持するbufferの挙動について記す。

c.sendline("echo 'LOVELY SPAAAAAAAAAAAAM!'")

# まず、expectをすると、
c.expect("SPA+M!")
# spawn.bufferの中から、expectで求められた文字列を探す。

# さて、2つ前のexpectではログイン後のプロンプトにマッチしていた為、
# 当然ながらechoをsendlineした時点でのc.bufferの中身は "" である。
# expectされた文字列がbufferに見つけらないと、
# pexpectは内部保持する文字列をmaxsizeの文字数だけ仮bufferに書き込む。
# 仮buffer = "echo 'LOVELY SPAAAAAAAAAAAAM!'\r\nLOVELY SPAAAAAAAAAAAAM!\r\nspam@blackknight:/export/home/spam(101)> "
# 書き込まれた仮bufferを与えられた正規表現を元に先頭から検索する。
# 例で言えば、ヒットするのは1回目のSPAAAAAAAAAAAAM!である。
# つまり、上のexpectの結果、最終的にafter before bufferの中身は以下の通りとなる。

print c.after # "SPAAAAAAAAAAAAM!"
print c.before # "echo 'LOVELY "
print c.buffer # "'\r\nLOVELY SPAAAAAAAAAAAAM!\r\nspam@blackknight:/export/home/spam(101)> "

# 恐らく、期待する挙動と違ったのでは無いだろうか。
# 期待する挙動は、echoコマンドの出力結果に対してのヒットであり、
# echoコマンドの引数にヒットではなかったはずだ。

# これでは、echoコマンドが正確に帰ってきたかどうかのテストにはならない。
# そんな時は、spawn.readline()を使うと良い。

c.expect(".*$") # 文末までの全てにマッチ == bufferをクリア
c.sendline("echo 'LOVELY SPAAAAAAAAAAAAM!'")
c.readline()

# spawn.readline()は、spawn.expect("\r\n")と等価（のはず）である。
# つまり、コマンド入力行の末尾にマッチするので、

print c.after # "\r\n"
print c.before # "echo 'LOVELY SPAAAAAAAAAAAAM!'"
print c.buffer # "LOVELY SPAAAAAAAAAAAAM!\r\nspam@blackknight:/export/home/spam(102)> "

# このようになる。
# こうなったら、心置きなくexpectすればよい。

c.expect("SPA+M!")

print c.after # "SPAAAAAAAAAAAAM!"
print c.before # "LOVELY "
print c.buffer # "\r\nspam@blackknight:/export/home/spam(102)> "

# pexpectを使う上では、このbufferの管理が非常に大事なようで、コイツを見失うと、厄介な事になりかねない。
# cdした後に、CWDとファイルの存在を確認した上で、rm -rf ./* 等の簡易スクリプトを組んだ際、
# expectが発行したコマンドの引数にヒットしていて、実は・・・なんてことが起これば悪夢である。

c.sendline("exit")
c.expect(pexpect.EOF)
c.close()
