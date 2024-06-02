#!/usr/bin/python3
# pxssh を利用した "su -" のテスト
import sys
import re

import pexpect 
from pexpect import pxssh

def login_ssh(server: str, username: str, password: str):
    # ログイン情報を設定しSSHサーバーにログイン
    ssh = pxssh.pxssh(options={
                    "StrictHostKeyChecking": "no",
                    "UserKnownHostsFile": "/dev/null"})

    # プロンプトの設定 (オプション)
    ssh.UNIQUE_PROMPT = r"[\$\#] "
    ssh.PROMPT = ssh.UNIQUE_PROMPT
    ssh.PROMPT_SET_SH = r"PS1='\$ '"
    ssh.PROMPT_SET_CSH = r"set prompt='\$ '"
    ssh.PROMPT_SET_ZSH = "prompt restore;\nPS1='%(!.#.$) '"

    ssh.login(server=server,
            username=username,
            password=password,
            port=22)
    #print(ssh.before.decode(encoding='utf-8'), flush=True, end="")
    #print(ssh.after.decode(encoding='utf-8'), flush=True, end="")
    #while True:
    #    index = ssh.expect_list(
    #        [
    #            re.compile(r".*(#|\$) ".encode()),   # 一般ユーザーまたはroot ユーザーのプロンプト
    #            re.compile(r"\n".encode()),
    #        ], timeout = 10)
    #    print(ssh.before.decode(encoding='utf-8'), flush=True, end="")
    #    print(ssh.after.decode(encoding='utf-8'), flush=True, end="")
    #    if index == 0:
    #        break
    while True:
        try:
            while True:
                index = ssh.expect_list(
                    [
                        re.compile(r".*(#|\$) ".encode()),   # 一般ユーザーまたはroot ユーザーのプロンプト
                        re.compile(r"\n".encode()),
                    ], timeout = 1)
                #print(ssh.before.decode(encoding='utf-8'), flush=True, end="")
                print(ssh.after.decode(encoding='utf-8'), flush=True, end="")
                if index == 0:
                    break
        except Exception as e:
              #print(e)
              break
    return ssh

def sendline_and_print(ssh, command: str):
    print(f"{command}")
    ssh.sendline(command)

def run_command(ssh, command: str ,out):
    #sendline_and_print(ssh, command)
    ssh.sendline(command)
    try:
       # プロンプトが表示されるまで待つ
       while True:
           index = ssh.expect_list(
               [
                   re.compile(r".*(#|\$) ".encode()),   # 一般ユーザーまたはroot ユーザーのプロンプト
                   re.compile(r"\n".encode()),
               ], timeout = 10)
           print(ssh.before.decode(encoding='utf-8'), flush=True, end="", file=out)
           print(ssh.after.decode(encoding='utf-8'), flush=True, end="" , file=out)
           if index == 0:
               break
    except pexpect.exceptions.EOF:
        print("EOF")

def send_commands(ssh):
    run_command(ssh, "touch test.txt")
    run_command(ssh, "ls -l")

def switch_to_root(ssh, root_pass: str):
    sendline_and_print(ssh, "su -")

    # rootのパスワードを入力するプロンプトが表示されるまで待つ
    ssh.expect(r".*: ")
    #print(ssh.before.decode(encoding='utf-8'), flush=True, end="")
    #print(ssh.after.decode(encoding='utf-8'), flush=True, end="")

    ssh.sendline(root_pass)

    # root ユーザーのプロンプトが表示されるまで待つ
    index = ssh.expect_list(
        [
            re.compile(r".*# ".encode()),   # root ユーザーのプロンプト
            re.compile(r"su: .*".encode()), # "su: Authentication failure" or "su: 認証失敗"
        ], timeout = 10)
    if index != 0:
        print("failed to switch to root")
        sys.exit(1)
    #print(ssh.before.decode(encoding='utf-8'), flush=True, end="")
    #print(ssh.after.decode(encoding='utf-8'), flush=True, end="")

def send_commands_root(ssh):
    run_command(ssh, "ls -l")
    #run_command(ssh, "find /etc")

    run_command(ssh, "id")
    run_command(ssh, "exit")

def send_commands_by_cmdfile(ssh, cmdfile, out):
    with open(cmdfile,encoding='utf-8')as f:
        cmdlist= f.readlines()
        for cmd in cmdlist:
            cmd_ = cmd.rstrip().lstrip()
            if cmd_.startswith('#'):
               continue
            if cmd_ != '':
               #print("------------- " + cmd_)
               run_command(ssh, cmd_, out)

    run_command(ssh, "exit", out)

def root_command_exec(server, username, password, root_pass, cmd_file, out):
    ssh = login_ssh(server, username, password)
    switch_to_root(ssh, root_pass=root_pass)
    send_commands_by_cmdfile(ssh, cmd_file, out)
    ssh.logout()

def user_command_exec(server, username, password, cmd_file, out):
    ssh = login_ssh(server, username, password)
    send_commands_by_cmdfile(ssh, cmd_file, out)
    ssh.logout()


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print(f"Usage: python3 {sys.argv[0]} <server> -u <username> <password>  <cmd_file>")
        print(f"Usage: python3 {sys.argv[0]} <server> -r <username> <password> <root_password> <cmd_file>")
        sys.exit(1)

    if sys.argv[2] == '-r' :
       server = sys.argv[1]
       username = sys.argv[3]
       password = sys.argv[4]
       root_pass = sys.argv[5]
       cmd_file = sys.argv[6]
       if  len(sys.argv) == 7:
           out = sys.stdout
       elif  len(sys.argv) == 8:
           save_file = sys.argv[7]
           out = open(save_file, mode='w')
       else:
           sys.exit()

       root_command_exec(server, username, password, root_pass, cmd_file, out)

    elif sys.argv[2] == '-u' :
       server = sys.argv[1]
       username = sys.argv[3]
       password = sys.argv[4]
       cmd_file = sys.argv[5]
       if  len(sys.argv) == 6:
           out = sys.stdout
       elif  len(sys.argv) == 7:
           save_file = sys.argv[6]
           out = open(save_file, mode='w')
       else:
           sys.exit()
       
       user_command_exec(server, username, password, cmd_file, out)

