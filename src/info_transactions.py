from pandas import read_csv, read_excel


def transactions_csv(df_csv):
    """
    Функция для вывода данных из csv файла в список со словарями.
    """
    try:
        result_df_csv = df_csv.to_dict(orient="records")
        return result_df_csv
    except Exception:
        return "Данного файла не существует"


def transactions_xlsx(df_excel):
    """
    Функция для вывода данных из xlsx файла в список со словарями.
    """
    try:
        result_df_excel = df_excel.to_dict(orient="records")
        return result_df_excel
    except Exception:
        return "Данного файла не существует"


if __name__ == "__main__":
    df_csv = read_csv("../data/transactions.csv")
    df_excel = read_excel("../data/transactions_excel.xlsx")
    print("Файл csv")
    print(transactions_csv(df_csv))
    print("Файл xlsx")
    print(transactions_xlsx(df_excel))
