from datetime import date
from ftplib import FTP, all_errors


def csv_ftp_download(host='', port=0, user='', passwd='', remote_file='', local_file=''):
    ftp = FTP()
    try:
        ftp.connect(host=host, port=port, timeout=10)
        ftp.login(user=user, passwd=passwd)
    except all_errors as e:
        raise e

    # print working directory
    pwd_path = ftp.pwd()
    print("FTP当前路径:", pwd_path)
    ftp.cwd('tj_yd_csv')
    # with open(local_file, 'wb') as f:
    #     try:
    #         ftp.retrbinary(remote_file, f.write)
    #     except all_errors as e:
    #         print(e)
    #         raise e


if __name__ == "__main__":
    host = 'host'
    port = 21
    user = 'username'
    passwd = 'password'
    ftp_relative_path = 'tj_yd_csv'

    prefix_file = 'cm_cell_'
    suffix_file = '.csv'
    today = date.today().strftime('%Y%m%d')
    file_name = f"{prefix_file}{today}{suffix_file}"
    remote_file = f'RETR {ftp_relative_path}/{file_name}'
    local_file = f'csv/{file_name}'

    print(file_name)

    csv_ftp_download(host=host,
                     port=port,
                     user=user,
                     passwd=passwd,
                     remote_file=remote_file,
                     local_file=local_file)

