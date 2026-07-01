# Путь к папкам с файлами
DATA_DIR = "data"
REPORTS_DIR = "reports"
LOGS_DIR = "logs"

# Настройки для фильтрации статусов
STATUS_COLUMN = 'status'
TARGET_STATUS = 'Delivered'
AMOUNT_COLUMN = 'total_amount'

# Имя итового файла
OUTPUT_FILE_NAME = 'summary_report.csv'

# обязательные колонки в файле
REQUIRED_COLUMNS = [AMOUNT_COLUMN, STATUS_COLUMN]
