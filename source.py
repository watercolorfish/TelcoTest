import datetime
import sqlite3
#import MySQLdb
import mysql.connector
#import os
import paramiko

if __name__ == "__main__":
    a = input()
    file = open(a, 'r')
    for line in file:
        if (line.startswith('sftp_host')):
            host = (line.split('='))[1].split('\n')[0]
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
        if (line.startswith('sql_user')):
            sql_user = (line.split('='))[1].split('\n')[0]
        if (line.startswith('sql_password')):
            sql_password = (line.split('='))[1].split('\n')[0]
        if (line.startswith('sql_database')):
            sql_database = (line.split('='))[1].split('\n')[0]

    file.close()

    #files = os.listdir(directory)

    conn = mysql.connect(user=sql_user, passwd=sql_password, db=sql_database)
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXIST information
                      (date and time, name of file)
                   """)
    conn.commit()

    transport = paramiko.Transport((host, port))
    transport.connect(username=user, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)

    ftp = sftp.open_sftp()
    ftp.chdir(directory)
    files = ftp.listdir()

    for remote_dir in files:
        sftp.get(remote_dir, local_dir)
        now = datetime.datetime.now()
        now.strftime("%d-%m-%Y %H:%M")
        cursor.executemany("INSERT INTO albums VALUES (?,?)", (now, remote_dir))

    sftp.close()
    transport.close()
