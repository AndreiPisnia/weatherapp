import prettytable

from weatherapp.core.abstract import Formatter

class TableFormatter(Formatter):
    """Table formatter for app output.
    """

    def emit(self, column_names, data):
        """Format and print data from the iterable source.

        :param column_names: names of the columns
        :type column_names: list
        :param data: iterable data source, one tuple per object
                     with value in order of column names
        :type data: list or tuple
#        :param stdout: output stream where data should be written
#        :type stdout: sys.stdout or file like object
        """

        pt = prettytable.PrettyTable()
        
        for column, values in zip(column_names, (data.keys(), data.values())):
            if any(values):
                pt.add_column(column, list(values))

        return pt.get_string()
