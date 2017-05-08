import xlsxwriter

class ExcelBook():
    def __init__(self, manufacturer = 'all'):
        self.workbook = xlsxwriter.Workbook(manufacturer + '.xlsx')
        self.worksheet = self.workbook.add_worksheet()
        self.columNames = ["ID", "manufactureName", "modelNumber", "modelPrice", "productName", "productDescription", "imageLocation", "URL", "productCondition", "availability", "googleProductCategory"]

    def populateTable(self, tableData):
        tableData.insert(0, self.columNames)
        for row in range(0, len(tableData)):
            for col in range(0, len(tableData[row])):
                self.worksheet.write(row, col, tableData[row][col])        

    def close(self):
        self.workbook.close()
