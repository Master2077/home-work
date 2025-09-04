import inspect
import time
from functools import wraps


def log():
    """
        Декоратор для логирования информации о вызовах функций.

        Возвращает обертку, которая записывает имя функции, результат её выполнения,
        время выполнения и информацию об ошибках, если они возникают.
        """
    def wrapper(function):
        @wraps(function)
        def inner(*args, **kwargs):
            """
                Функция с основной логикой работы
            """
            # Выполняется если внешняя функция не выдает ошибок
            try:
                result = function(*args, **kwargs)  # Вызываем оригинальную функцию
                start_time = time.time()    # Запоминаем время начала выполнения
                print(f"Функция: {function.__name__}")  # Выводим имя функции
                print(f"Результат: {result}") # Выводим результат выполнения
                end_time = time.time()   # Запоминаем время окончания выполнения
                print(f"Время выполнения: {end_time - start_time}")  # Выводим время выполнения
            # Выполняется если внешняя функция выдает ошибку
            except Exception as e:
                start_time = time.time()    # Запоминаем время начала выполнения
                print(f"Функция: {function.__name__}")  # Выводим имя функции
                print(f"Ошибка: {e}")   # Выводим тип ошибки
                print(f"Входные параметры: {inspect.getcallargs(my_function, *args, **kwargs)}")    # Выводим входные параметры
                end_time = time.time()  # Запоминаем время окончания выполнения
                print(f"Время выполнения: {end_time - start_time}") # Выводим время выполнения

        return inner    # Возвращаем обертку

    return wrapper  # Возвращаем декоратор


@log()
def my_function(x, y):
  """
    x делим на y
  """
  return x / y

# Вызов функции
my_function(0, 0)
