import unittest
import os
import csv
from ViewPersonalData import PersonalDataViewer


class TestPersonalDataViewer(unittest.TestCase):
    def setUp(self):
        self.file_name = os.path.join(os.path.dirname(__file__), "Data", "data_sample_1.csv")
        self.open_file = open(self.file_name, 'r')
        self.pdv = PersonalDataViewer([self.open_file])

        open_file = open(self.file_name, 'r')
        self.data = {self.file_name: list(csv.reader(open_file))}

    def test_file(self):
        # Makes sure the file is closed
        self.assertRaises(ValueError, self.open_file.seek, 0)

    def test_data(self):
        self.assertTrue(self.pdv.data)
        self.assertIsInstance(self.pdv.data, dict)
        self.assertIn(self.file_name, self.pdv.data)


        self.assertListEqual(self.pdv.headers(self.file_name), self.data[self.file_name][0])

    def test_manipulate_data(self):
        entries = ["Rita",
                   "Lin",
                   "Animal Logic",
                   "1405-6838 Station Hill Drive",
                   "Burnaby",
                   "British Columbia",
                   "V3N 5A4",
                   "778-999-1899",
                   "greenlin.name@gmail.com",
                   "https://rita-lin-vfx.blogspot.com"]

        self.pdv.addEntries(self.file_name, entries)
        self.assertIn(entries, self.pdv.data[self.file_name])

    def test_write_data(self):
        self.assertTrue(self.pdv.generateHtmlCode().startswith("<html>"))
        self.assertTrue(self.pdv.generateHtmlCode().endswith("</html>"))

        html_file = os.path.join(os.path.dirname(__file__), "ViewPersonalDataUnitTestFiles", "personal_data.html")
        self.pdv.show(output_dir=os.path.dirname(html_file), launch=False)
        self.assertTrue(os.path.exists(html_file))

        csv_file = os.path.join(os.path.dirname(__file__), "ViewPersonalDataUnitTestFiles", "data_sample_1.csv")
        self.pdv.show(format_style="csv", output_dir=os.path.dirname(html_file), launch=False)
        self.assertTrue(os.path.exists(csv_file))


if __name__ == "__main__":
    unittest.main()