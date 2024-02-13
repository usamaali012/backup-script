import os
import time
from datetime import datetime
import subprocess

from dotenv import load_dotenv


def backup_mysql_database():
    backup_dir = os.getenv('MYSQL_BACKUP_DIR')

    os.makedirs(backup_dir, exist_ok=True)

    now = time.time()

    dt = datetime.fromtimestamp(now)
    fd = dt.strftime('%d%m%Y')

    db_config = {
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST_MAIN'),
        'database': os.getenv('DB_NAME')
    }

    output_file_path = f'{backup_dir}/{db_config["database"]}-{fd}.sql.gz'

    # Connect to the MySQL database
    mysqldump_cmd = (f"mysqldump -u{db_config['user']} -p{db_config['password']} {db_config['database']} "
                     f"| gzip > {output_file_path}")

    try:
        subprocess.run(mysqldump_cmd, shell=True, check=True)
        print(f"Backup completed successfully. Output saved to {output_file_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    load_dotenv(verbose=True)

    backup_mysql_database()

