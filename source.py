#import sqlite3
import os
import paramiko

if __name__ == "__main__":
    a = input("Путь к файлу: ")
    arr = []
    file = open(a, 'r')
    for line in file:
        arr.append(line)
    file.close()
    print(arr)
    for str in arr:
        if (str.startswith('sftp_host')):
            host = (str.split('='))[1].split('\n')[0]
        if (str.startswith('sftp_port')):
            port = (str.split('='))[1].split('\n')[0]
        if (str.startswith('sftp_user')):
            user = (str.split('='))[1].split('\n')[0]
        if (str.startswith('sftp_password')):
            password = (str.split('='))[1].split('\n')[0]
        if (str.startswith('sftp_remote_dir')):
            directory = (str.split('='))[1].split('\n')[0]
        if (str.startswith('local_dir')):
            local_dir = (str.split('='))[1].split('\n')[0]

    files = os.listdir(directory)

    transport = paramiko.Transport((host, port))
    transport.connect(username=user, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)

    for remote_dir in files:
        remotepath = remote_dir

        sftp.get(remotepath, local_dir)
        sftp.put(local_dir, remotepath)

    sftp.close()
    transport.close()
