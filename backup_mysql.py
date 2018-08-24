import subprocess
import datetime
import sys
import os
import paramiko

DB_NAME = "rvchub"
DB_USER = "rvchub"
DB_PASS = "password"

SSH_HOST = "host"
SSH_USER = "root"
SSH_PASSWRD = "password"
SSH_PORT = 22

DUMP_BASE_NAME = "rvchub.sql"
REMOTE_DUMP_PATH = "/root/rvchub_backup/"


def ssh_connect():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(hostname=SSH_HOST, username=SSH_USER, password=SSH_PASSWRD, port=SSH_PORT, timeout=30)
    except:
        print("CONNECTION ERROR")
        cleanup(dump_name)
    return client


def ssh_close(client):
    client.close()


def cleanup(dump_name):
    subprocess.call(["rm", "-f", dump_name])
    subprocess.call(["rm", "-f", dump_name + ".tar.gz"])
    sys.exit()


def make_dump_name():
    today = datetime.datetime.today()
    dump_name = "{}-{:02d}-{:02d}_{}".format(today.year, today.month, today.day, DUMP_BASE_NAME)
    return dump_name


def make_dump(dump_name):
    try:
        retcode = subprocess.call(["mysqldump", DB_NAME, "-u{}".format(DB_USER),  "-p{}".format(DB_PASS), "--result-file={}".format(dump_name)])
        if retcode != 0:
            print("MYSQL: ERROR", retcode)
            cleanup(dump_name)
    except OSError:
        print("MYSQL: OS ERROR")
        cleanup(dump_name)


def tar_dump(dump_name):
    try:
       retcode = subprocess.call(["tar", "-zcf", "{}.tar.gz".format(dump_name), dump_name])
       if retcode != 0:
            print("TAR: ERROR")
            cleanup(dump_name)
    except OSError:
        print("TAR: OS ERROR")
        cleanup(dump_name)
 

def send_dump(client, dump_name):
    try:
        source_file = dump_name + ".tar.gz"
        target_file =  os.path.join(REMOTE_DUMP_PATH, dump_name  + ".tar.gz")
        sftp = client.open_sftp()
        sftp.put(source_file, target_file)
    except:
        print("SENDING ERROR")
        ssh_close(client)
        cleanup(dump_name)


def get_dumps_list(client):
    stdin, stdout, stderr = client.exec_command('cd {}&&ls -1'.format(REMOTE_DUMP_PATH))
    data = stdout.read().decode().split()
    return data


def select_files_to_remove(files):
    today = datetime.datetime.today()

    keep_days = datetime.timedelta(days=30)
    keep_years = datetime.timedelta(days=370)

    last_keep_day = today - keep_days
    last_keep_year = today - keep_years

    res = list()
    for d in files:
        date = d.split('_')[0]
        date = datetime.datetime.strptime(date, '%Y-%m-%d')
        if (date < last_keep_day and date.day != 1) or (date < last_keep_day and date.day != 1 and date.month != 12):
            res.append(d)
    return res


def main():
    dump_name = make_dump_name()

    make_dump(dump_name)
    tar_dump(dump_name)

    ssh = ssh_connect()
    send_dump(ssh, dump_name)

    files = get_dumps_list(ssh)
    print(files)
    print(select_files_to_remove(files))

    ssh_close(ssh)

main()

