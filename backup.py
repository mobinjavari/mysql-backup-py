from datetime import datetime
import os


class mysql_backup:
    _last_backup_file = None
    _backup_dir = '/home/mysql_backup'

    @staticmethod
    def print_log(text):
        print(f"---- {text} ----")

    @property
    def backup_dir(self):
        if not os.path.isdir(self._backup_dir):
            os.mkdir(self._backup_dir)
            mysql_backup.print_log('Create Backup Folder')

        mysql_backup.print_log(f"Backup DIR {self._backup_dir}")

        return self._backup_dir

    @property
    def file_template(self):
        datetime_now = datetime.now().strftime("%Y-%m-%d~%H:%M:%S")
        backup_file = f"{self.backup_dir}/backup[{datetime_now}].sql"
        self._last_backup_file = backup_file
        mysql_backup.print_log(f"File Template {backup_file}")

        return backup_file

    def create_backup(self, db_name, db_user='root', db_password=''):
        dump_cmd = f"mysqldump -u{db_user} -p{db_password} {db_name} > {self.file_template}"
        os.system(dump_cmd)
        mysql_backup.print_log(f"Create New Backup {self._last_backup_file}")

    @property
    def last_backup_file(self):
        return self._last_backup_file
