import json
import htmllib


class PersonalData(object):
    def __init__(self, data):
        self.__data = data
        self.__dataError = None
        self.validateData()

    def validateData(self):
        """
        Validates input data by checking that there
        :return:
        """
        if not self.__data:
            self.__dataError = "No data input specified"
            return False

        data_line = self.__data.split("\n")
        if len(data_line) < 2:
            self.__dataError = "Data needs at least a header and at least one data entry"
            return False

        for index, data_line in enumerate(data_line):
            if len(self.headers) != len(data_line.split(",")):
                self.__dataError = "Data size mistmatch on line {}. ".format(index)
                self.__dataError += "Make sure the length of all entries match the length of the headers"
                return False

        self.__dataError = None
        return True


    @property
    def headers(self):
        return self.__data.split("\n")[0]

    @property
    def data(self):
        return self.__data.split("\n")[1:]
