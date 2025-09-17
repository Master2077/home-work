import inspect
import time
from functools import wraps


def log(filename=None):
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
            start_time = time.time()  # Запоминаем время начала выполнения
            try:
                result = function(*args, **kwargs)  # Вызываем оригинальную функцию
                end_time = time.time()  # Запоминаем время окончания выполнения

                log_message = (
                    f"\nФункция: {function.__name__}\n"
                    f"Результат: {result}\n"
                    f"Время выполнения: {end_time - start_time}\n"
                )

                if filename:
                    with open(filename, "a", encoding="utf-8") as log_file:
                        log_file.write(log_message)
                else:
                    return log_message

                return result
            except Exception as e:
                end_time = time.time()  # Запоминаем время окончания выполнения
                error_message = (
                    f"\nФункция: {function.__name__}\n"
                    f"Ошибка: {str(e)}\n"
                    f"Входные параметры: {inspect.getcallargs(function, *args, **kwargs)}\n"
                    f"Время выполнения: {end_time - start_time}\n"
                )
                if filename:
                    with open(filename, "a", encoding="utf-8") as log_file:
                        log_file.write(error_message)

                else:
                    print(error_message)

        return inner  # Возвращаем обертку

    return wrapper  # Возвращаем декоратор


@log()  # Убедитесь, что вы вызываете декоратор с ()
def my_function(x, y):
    """
    Делит x на y.
    """
    return x / y


# Вызов функции
print(my_function(10, 0))