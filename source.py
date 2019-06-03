import datetime
import sqlite3
import os
import paramiko

if __name__ == "__main__":
    a = input("Путь к файлу: ")
    file = open(a, 'r')
    for line in file:
        if (line.startswith('sftp_host')):
            host = (line.split('='))[1].split('\n')[0]
            print(host)
        if (line.startswith('sftp_port')):
            port = (line.split('='))[1].split('\n')[0]
        if (line.startswith('sftp_user')):
            user = (line.split('='))[1].split('\n')[0]
        if (line.startswith('sftp_password')):
            password = (line.split('='))[1].split('\n')[0]
        if (line.startswith('sftp_remote_dir')):
            directory = (line.split('='))[1].split('\n')[0]
        if (line.startswith('local_dir')):
            local_dir = (line.split('='))[1].split('\n')[0]
            print(local_dir)
        #arr.append(line)
    file.close()

    files = os.listdir(directory)

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE information
                      (date and time, name of file)
                   """)

    transport = paramiko.Transport((host, port))
    transport.connect(username=user, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)

    for remote_dir in files:
        remotepath = remote_dir

        sftp.get(remotepath, local_dir)
        sftp.put(local_dir, remotepath)
        now = datetime.datetime.now()
        now.strftime("%d-%m-%Y %H:%M")

    sftp.close()
    transport.close()
