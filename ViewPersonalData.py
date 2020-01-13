import sys
import os
import argparse
import webbrowser
import csv
import subprocess
import pprint


class PersonalDataViewer(object):
    """
    Reads csv files provided from arguments in the command line

    """
    def __init__(self, in_files):
        """
        Reads data from files and organizes it in an python dictionary
        :param in_files: file - files to read
        """
        self.__data = {}
        for fileread in in_files:
            filename = os.path.abspath(fileread.name)
            reader = list(csv.reader(fileread))
            self.__data.update({filename: reader})
            fileread.close()
        self.supported_formats = ["html", "csv", "text"]

    @property
    def data(self):
        return self.__data

    def addEntries(self, filename, *arguments):
        """
        Adds entries to dataset
        :param filename: str - path to the file to add entries to
        :param arguments: iterable - list of itms to add to the dataset
        """
        self.__data[filename].append(*arguments)

    def headers(self, filename):
        """
        Retutns the headers of the dataset of the given file
        :param filename: str - path to the file to add entries to
        :return: list - list of header items at the top of the table
        """
        return self.__data[filename][0]

    def generateHtmlCode(self):
        """
        Maps the internal ptyhon data set to an html table
        :return: str - html code representing the dataset
        """
        html = '<html>\n'
        for filename, data in sorted(self.__data.items()):
            html += '\t<h1>{0}</h1>\n\t<table border="1">\n\t\t<tr>\n'.format(filename)
            for header in data[0]:
                html += '\t\t\t<th>{0}</th>\n'.format(header)
            html += '\t\t</tr>\n'
            for entry in data[1:]:
                html += '\t\t<tr>\n'
                for item in entry:
                    html += '\t\t\t<td>{0}</td>\n'.format(item)
                html += '\t\t</tr>\n'
            html += '\t</table>\n'
        html += "</html>"
        return html

    def writeToFile(self, file_contents, output_dir, filename, extension):
        """
        Writes the provided file contents to a file
        :param file_contents: str - file contents that will be writen on to a file
        :param output_dir: str - directory where the files will be placed. If one doesn't exist, it will be created
        :param filename: str - name of the output file
        :param extension: str - the extension of the filename. e.g. 'html'
        :return: str - file path of the newly created file
        """
        filename = os.path.join(output_dir, "{0}.{1}".format(filename, extension))
        if not os.path.exists(output_dir):
            print output_dir
            os.makedirs(output_dir)

        with open(filename, 'w') as f:
            f.write(file_contents)

        return filename

    def show(self, format_style="html", output_dir=os.path.dirname(__file__), launch=True):
        """
        Formats, writes and displays personal data in different formats
        :param format_style: str - "html", text, "csv"
        :param output_dir: str - file path to the output directory. If no argument is passed,
                                 it'll default to the current directory where this script resides
        :param launch: bool - weather or not to launch an application to display the data
        """
        # Write and display html
        if format_style == "html":
            html = self.generateHtmlCode()
            output_dir = os.path.abspath(output_dir)
            filename = self.writeToFile(html, output_dir, "personal_data", "html")
            if launch:
                if subprocess.check_call(['open', filename]):
                    webbrowser.open_new(filename)
            sys.stdout.write("\nFile generated: {0}\n".format(filename))

        # Write and display CSV
        elif format_style == "csv":
            for filename, filedata in self.__data.items():
                output_file = os.path.join(output_dir, os.path.basename(filename))
                with open(output_file, 'wb') as wb:
                    wr = csv.writer(wb, quoting=csv.QUOTE_ALL)
                    for entry in filedata:
                        wr.writerow(entry)
                if launch:
                    subprocess.check_call(['open', filename])
                sys.stdout.write("File generated: {0}\n".format(filename))

        # Display Text
        elif format_style == "text":
            sys.stdout.write(str(pprint.pprint(self.__data)))

        # Invalid format style
        else:
            sys.stderr.write("Format style not supported: {0}. Chose from 'html', 'csv', 'text'\n".format(format_style))


# Validate File
def isValidFile(parser, arg):
    """
    Checks to see if the file path provided in the arguments exists
    :param parser: ArgumentParser - the instantiated object of the argsparser
    :param arg: str - the path to a file that is supposed to exist
    :return: file - returns the file object of the file path
    """
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return open(arg, 'r')  # return an open file handle


# Is Directory Valid
class readable_dir(argparse.Action):
    """
    Check to see if the provided directory path is valid.
    """
    def __call__(self, parser, namespace, values, option_string=None):
        prospective_dir=values
        if not os.path.isdir(prospective_dir):
            raise argparse.ArgumentTypeError("readable_dir:{0} is not a valid path".format(prospective_dir))
        if os.access(prospective_dir, os.R_OK):
            setattr(namespace, self.dest, prospective_dir)
        else:
            raise argparse.ArgumentTypeError("readable_dir:{0} is not a readable dir".format(prospective_dir))


if __name__ == "__main__":
    # Argument Parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--inputFiles",
                        dest="filesIn",
                        required=True,
                        nargs='+',
                        help="Input file containing personal information entries",
                        metavar="FILE",
                        type=lambda x: isValidFile(parser, x))
    parser.add_argument("-o", "--outputDirectory",
                        dest="outDir",
                        help="Directory where files will output",
                        metavar="DIRECTORY",
                        type=readable_dir)
    parser.add_argument("-d", "--displayFormat",
                        help="Displays the data in this format. Options are: 'html', 'csv', 'text'")
    args = parser.parse_args()

    personal_data_viewer = PersonalDataViewer(args.filesIn)
    personal_data_viewer.show(args.displayFormat)