# app_home/management/commands/wait_for_db.py
import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Django command to pause execution until database is available"""

    def handle(self, *args, **options):
        self.stdout.write("Waiting for database...")
        db_conn = None
        max_attempts = 60  # Tăng số lần thử lên 60
        attempt = 0
        while not db_conn and attempt < max_attempts:
            try:
                connection = connections["default"]
                connection.cursor()  # Thử tạo cursor để kiểm tra kết nối thực sự
                db_conn = True
                logger.info("Database connection successful")
            except OperationalError as e:
                logger.warning(
                    f"Database unavailable, attempt {attempt + 1}/{max_attempts}: {str(e)}"
                )
                self.stdout.write(
                    f"Database unavailable, attempt {attempt + 1}/{max_attempts}, waiting 2 seconds..."
                )
                time.sleep(2)  # Tăng thời gian chờ lên 2 giây
                attempt += 1
            except Exception as e:
                logger.error(f"Unexpected error while connecting to database: {str(e)}")
                self.stdout.write(self.style.ERROR(f"Unexpected error: {str(e)}"))
                raise

        if not db_conn:
            error_msg = "Database connection failed after max attempts"
            logger.error(error_msg)
            self.stdout.write(self.style.ERROR(error_msg))
            raise Exception(error_msg)

        success_msg = "Database available!"
        logger.info(success_msg)
        self.stdout.write(self.style.SUCCESS(success_msg))
