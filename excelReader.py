import xlrd

class ExcelBook():
    def extractWorkbookData(self, manufactureName):
        #open the workbok
        workbook = xlrd.open_workbook('{}.xlsx'.format(manufactureName))
        #get the sheet
        worksheet = workbook.sheet_by_name('Sheet1')
        #find the number of rows
        num_rows = worksheet.nrows - 1
        #set cursor at top of page
        curr_row = 0

        #iterate through each row convert to usable list item
        worksheetValue = []
        while curr_row < num_rows:
            curr_row += 1
            worksheetRow = worksheet.row(curr_row)
            rowValue = []
            for cell in worksheetRow:
                if cell == worksheetRow[0]:
                    cellValue = long(cell.value)
                else:
                    cellValue= str(cell.value)
                rowValue.append(cellValue)
            worksheetValue.append(rowValue)
        
        return worksheetValue
                

