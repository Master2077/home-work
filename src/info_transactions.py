import pandas
from pandas import read_csv, read_excel


def transactions_csv(df_csv):
    """
    Функция для вывода данных из csv файла в список со словарями.
    """
    try:
        result_df_csv = df_csv.to_dict(orient="records")
        return result_df_csv
    except Exception:
        return "Ошибка"


def transactions_xlsx(df_excel):
    """
    Функция для вывода данных из xlsx файла в список со словарями.
    """
    try:
        result_df_excel = df_excel.to_dict(orient="records")
        return result_df_excel
    except Exception:
        return "Ошибка"


# Проверка валидонсти CSV файла
try:
    df_csv = read_csv("../data/transactions.csv")
    result_csv = transactions_csv(df_csv)
except FileNotFoundError:
    result_csv = "Файла не существует"
except pandas.errors.EmptyDataError:
    result_csv = "Файл пуст"
except Exception as e_csv:
    result_csv = f"Ошибка: {e_csv}"

# Проверка валидонсти XLSX файла
try:
    df_excel = read_excel("../data/transactions_excel.xlsx")
    result_xlsx = transactions_xlsx(df_excel)
except FileNotFoundError:
    result_xlsx = "Файла не существует"
except pandas.errors.EmptyDataError:
    result_xlsx = "Файл пуст"
except Exception as e_xlsx:
    result_xlsx = f"Ошибка: {e_xlsx}"

if __name__ == "__main__":
    print("Файл csv:")
    print(result_csv)
    print("Файл xlsx:")
    print(result_xlsx)
