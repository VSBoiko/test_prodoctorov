import json
import os
import urllib.request
from datetime import datetime
import logging

log_format = "%(asctime)s: [%(levelname)s] %(funcName)s(%(lineno)d) - %(message)s"
logging.basicConfig(
    filename="reports.log",
    level=logging.INFO,
    format=log_format,
    datefmt='%Y-%m-%d. %H:%M:%S',
)


def get_json_from_url(url: str) -> list:
    open_url = urllib.request.urlopen(url)
    json_data = list()
    if open_url.getcode() == 200:
        data = open_url.read()
        json_data = json.loads(data)
    else:
        logging.error(f'Ошибка при получении данных {open_url.getcode()}')

    return json_data


def main():
    logging.info("Начало работы скрипта______")

    # Объявление основных переменных
    users_url = "https://json.medrating.org/users"
    todos_url = "https://json.medrating.org/todos"
    reports_dir = "tasks"
    reports_dir_tmp = "tmp"

    # Удаляем директорию для временных файлов
    if os.path.exists(reports_dir_tmp):
        os.rmdir(reports_dir_tmp)
        logging.error("Временная папка удалена до создание отчета")

    # Создаем отчеты во временную директорию
    user_reports = Reports(users_url, todos_url, reports_dir_tmp)
    user_reports.create_reports()

    # созданные отчеты переносятся в основную директорию
    for user_id, report in user_reports.users_reports.items():
        tmp_report = report.file_path
        report.change_report_dir(reports_dir)
        if report.is_exists():
            report.rename_to_old_report()
        os.replace(tmp_report, report.file_path)
        logging.info(f"Отчет перенесем {tmp_report} => {report.file_path}")

    # удаляется временная директория
    os.rmdir(reports_dir_tmp)
    logging.info("Временная папка удалена")

    logging.info("______Конец работы скрипта")


class Report:
    def __init__(self, user: dict, todos: dict, report_dir: str):
        self.user = user
        self.todos = todos
        self.report_dir = report_dir

        self.file_name_no_ext = user["username"]
        self.file_name = f'{self.file_name_no_ext}.txt'
        self.file_path = os.path.join(report_dir, self.file_name)

        self.count = self.count_completed = self.count_uncompleted = 0
        self.count_todos()

    def change_report_dir(self, new_report_dir):
        self.report_dir = new_report_dir
        self.file_path = os.path.join(self.report_dir, self.file_name)

    def count_todos(self):
        todos = self.todos
        for todo in todos.values():
            self.count += 1
            if todo["completed"]:
                self.count_completed += 1
            else:
                self.count_uncompleted += 1

    def create_report_file(self):
        user, todos, report_file_path = self.user, self.todos, self.file_path
        if not (self.is_exists()):
            with open(report_file_path, 'w') as report:
                logging.info(f'Попытка создать отчет {report_file_path}')
                report_text = self.__create_report_text()
                report.write(report_text)
                logging.info(f'Создан отчет {report_file_path}')

    def is_exists(self):
        return os.path.exists(self.file_path)

    def rename_to_old_report(self):
        path_to_report = self.file_path
        with open(path_to_report, 'r') as report:
            report.readline()
            second_line = report.readline()
            second_line_list = second_line.split(" ")
            report_date = second_line_list[-2].strip().replace(".", "-")
            report_time = second_line_list[-1].strip().replace(":", "-")
            new_file_name = f'old_{self.file_name_no_ext}_{report_date}T{report_time}.txt'
            new_path_to_report = os.path.join(self.report_dir, new_file_name)

        os.rename(path_to_report, new_path_to_report)
        logging.info(f'Отчет переименован: {path_to_report} -> {new_path_to_report}')

    def __create_report_text(self) -> str:
        user, todos = self.user, self.todos
        report_date = datetime.now().strftime("%d.%m.%Y %H:%M")
        completed_text = self.__create_report_text_todos(True)
        uncompleted_text = self.__create_report_text_todos(False)

        if self.count > 0:
            report_text = f'Отчет для {user["company"]["name"]}.\n' \
                          f'{user["name"]} <{user["email"]}> {report_date}\n' \
                          f'Всего задач: {self.count}\n' \
                          f'\n' \
                          f'Завершённые задачи ({self.count_completed}):\n' \
                          f'{completed_text}' \
                          f'\n' \
                          f'Оставшиеся задачи ({self.count_uncompleted}):\n' \
                          f'{uncompleted_text}'
        else:
            report_text = f'Отчет для {user["company"]["name"]}.\n' \
                          f'{user["name"]} <{user["email"]}> {report_date}\n' \
                          f'Задач нет\n'

        return report_text

    def __create_report_text_todos(self, completed: bool = True):
        todos = self.todos
        todos_text = ""
        for todo in todos.values():
            if todo["completed"] == completed:
                if len(todo["title"]) <= 48:
                    todos_text += f'{todo["title"]}\n'
                else:
                    todos_text += f'{todo["title"][0:48]}...\n'

        return todos_text


class Reports:

    def __init__(self, users_url: str, todos_url: str, reports_dir: str = "tasks"):
        self.users_url = users_url
        self.todos_url = todos_url
        self.reports_dir = reports_dir
        self.users = self.__create_users_dict()
        self.todos = self.__create_todos_dict()
        self.users_reports = {}

    def create_reports(self):
        if not (os.path.exists(self.reports_dir)):
            os.mkdir(self.reports_dir)
            logging.info(f'Создана директория {self.reports_dir}/')

        users, todos = self.users, self.todos
        for user_id, user in users.items():
            new_report = Report(user, todos[user_id], self.reports_dir)
            if new_report.is_exists():
                new_report.rename_to_old_report()
            new_report.create_report_file()
            self.users_reports[user_id] = new_report

    def __create_todos_dict(self) -> dict:
        todos = get_json_from_url(self.todos_url)
        todos_dict = dict()
        for todo in todos:
            if ("id" in todo) and ("userId" in todo):
                user_id, todo_id = todo["userId"], todo["id"]
                if not (user_id in todos_dict):
                    todos_dict.update({user_id: {}})
                todos_dict[user_id].update({todo_id: {}})
                todos_dict[user_id][todo_id] = todo.copy()

        return todos_dict

    def __create_users_dict(self) -> dict:
        users = get_json_from_url(self.users_url)
        users_dict = dict()
        for user in users:
            if "id" in user:
                user_id = user["id"]
                if not (user_id in users_dict):
                    users_dict.update({user_id: {}})
                users_dict[user_id] = user.copy()

        return users_dict


if __name__ == "__main__":
    main()
