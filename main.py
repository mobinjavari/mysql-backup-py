from flask import Flask, send_file, abort, request
from backup import mysql_backup
import os
import ipaddress

app = Flask(__name__)
backup = mysql_backup()


def check_telegram_request() -> bool:
    telegram_ip_ranges = [
        {'lower': '149.154.160.0', 'upper': '149.154.175.255'},
        {'lower': '91.108.4.0', 'upper': '91.108.7.255'}
    ]
    ip_addr = int(ipaddress.IPv4Address(request.remote_addr))

    for telegram_ip_range in telegram_ip_ranges:
        lower_dec = int(ipaddress.IPv4Address(telegram_ip_range['lower']))
        upper_dec = int(ipaddress.IPv4Address(telegram_ip_range['upper']))
        if lower_dec <= ip_addr <= upper_dec:
            return True

    return False


@app.route('/last_backup.sql')
def last_backup():
    # if check_telegram_request() is False:
    #     abort(403)

    backup.create_backup('MySQL_DB', 'MySQL_USER', 'MySQL_PASS')

    if not os.path.exists(backup.last_backup_file):
        abort(404, description="Error to Create Backup")

    return send_file(backup.last_backup_file, as_attachment=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=44600)


