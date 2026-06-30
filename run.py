import config
from src.analyzer import OrderAnalyzer


def main():
    analyzer = OrderAnalyzer(config)
    success_count, error_count = analyzer.process_all_files()
    print(f"Успешно обработанных файлов: {success_count}")
    print(f"Файлов с ошибкой: {error_count}")
    print(f"Всего найдено файлов: {success_count + error_count}")


if __name__ == "__main__":
    main()
