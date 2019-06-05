import datetime
import mysql.connector
import paramiko
from sys import argv

if __name__ == "__main__":
    script, first = argv
    file = open(first, 'r')
    for line in file:
        if (line.startswith('sftp_host')):
            host = (line.split('='))[1].split('\n')[0]
        if (line.startswith('sftp_port')):
            port = int((line.split('='))[1].split('\n')[0])
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

    conn = mysql.connector.connect(user=sql_user, passwd=sql_password, db=sql_database)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `information` (date_and_time DATETIME, name_of_file TEXT)")
    conn.commit()

    transport = None
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
        print(now, " ", remote_dir)
        cursor.executemany("INSERT INTO information VALUES (?,?)", (now, remote_dir))

    sftp.close()
    transport.close()

    cursor.execute("SELECT name of file, date and time FROM information")
    row = cursor.fetchone()
    while row is not None:
        print(row)
        row = cursor.fetchone()
    cursor.close()
    conn.close()
