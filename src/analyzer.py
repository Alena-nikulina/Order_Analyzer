from pathlib import Path
import pandas as pd
import os
import csv
import config
import logging


class OrderAnalyzer:
    def __init__(self, config):
        self.data_dir = config.DATA_DIR
        self.reports_dir = config.REPORTS_DIR
        self.logs_dir = config.LOGS_DIR

        self.status_column = config.STATUS_COLUMN
        self.target_status = config.TARGET_STATUS
        self.output_file_name = config.OUTPUT_FILE_NAME

        log_file_path = os.path.join(self.logs_dir, "errors.log")
        logging.basicConfig(
            filename=log_file_path,
            level=logging.ERROR,
            format="%(asctime)s - %(levelname)s - %(message)s",
            encoding="utf-8"
        )
        print("Класс OrderAnalyzer успешно инициализирован.")

    def load_file(self, filepath):
        # Загрузка csv-файла с обработкой исключений
        path = Path(filepath)
        try:
            df = pd.read_csv(path)
            if df.empty:
                logging.error(f"Файл {path.name} пуст")
                return None
            return df
        except Exception as e:
            logging.error(f"Ошибка при загрузке файла {path.name}: {e}")
            return None

    def filter_orders(self, df):
        # Фильтрация данных
        if self.status_column not in df.columns:
            logging.error(f"Колонка {self.status_column} не найдена в файле.")
            return pd.DataFrame()

        filtered_df = df[df[self.status_column] == self.target_status]
        return filtered_df

    def calculate_metrics(self, df, file_name):
        # Рассчет метрик и проверка устойчивости к не числовым данным
        metrics = {}
        df_clean = df.copy()

        # проверка, есть ли пустые значения в колонке total_amount
        was_nan_initially = df_clean['total_amount'].isna().any()
        df_clean['total_amount'] = pd.to_numeric(df_clean['total_amount'], errors='coerce')

        # если появились значения NaN - значит, в колонке были текстовые значения
        if not was_nan_initially and df_clean['total_amount'].isna().any():
            logging.error(f"Файл {file_name} пропущен, так как обнаружены нечисловые значения в total_amount.")
            return None

        total_revenue = round(df_clean['total_amount'].sum(), 2)
        avg_check = round(df_clean['total_amount'].mean(), 2)
        order_count = len(df_clean)

        metrics['file_name'] = file_name
        metrics['total_revenue'] = total_revenue
        metrics['avg_check'] = avg_check
        metrics['order_count'] = order_count

        return metrics

    def process_single_file(self, filepath):
        # Обработка одного файла
        path = Path(filepath)
        file_name = path.name
        df = self.load_file(path)
        if df is None:
            return None

        filtered_df = self.filter_orders(df)
        metrics = self.calculate_metrics(filtered_df, file_name)
        return metrics

    def process_all_files(self):
        # Пакетная обработка всех CSV-файлов в папке
        folder_path = Path(self.data_dir)
        csv_files = list(folder_path.glob('*.csv'))

        if not csv_files:
            print(f"В папке {self.data_dir} не найдено csv-файлов")
            return 0, 0  # возвращаем 0 успешных и 0 с ошибкой

        all_metrics = []
        success_count = 0  # успешные
        error_count = 0  # с ошибкой

        for filepath in csv_files:
            metrics = self.process_single_file(filepath)
            if metrics is None:
                error_count += 1
                continue

            all_metrics.append(metrics)
            success_count += 1

        # сохранение результатов в файл
        if all_metrics:
            report_df = pd.DataFrame(all_metrics)
            output_file_path = os.path.join(self.reports_dir, self.output_file_name)

            report_df.to_csv(output_file_path, index=False, encoding='utf-8')
            print(f"Итоговый отчет сохранен в {output_file_path}")
        else:
            print("Отчет не создан, так как все файлы содержат ошибки")

        return success_count, error_count
