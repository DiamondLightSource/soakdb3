class Cursor:
    def __init__(self, data_source_file):
        self.__data_source_file = data_source_file

    def execute(self, sql):
        pass

    def fetchall(self):
        pass

    def description(self):
        pass


class Connection:
    def __init__(self, data_source_file):
        self.__data_source_file = data_source_file

        self.row_factory = None

    def commit(self):
        pass

    def cursor(self):
        return Cursor(self.__data_source_file)


def connect(data_source_file):
    return Connection(data_source_file)
