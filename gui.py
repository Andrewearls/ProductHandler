from Tkinter import *
import SQLConnector
import excelReader
import excelWriting
class Application(Frame):

    def createWidgets(self):
        #quit button
        self.QUIT = Button(self, text="QUIT", command= self.quit)        

        #Create Excel file button
        self.CreateExcel = Button(self, text="Create Excel", command=self.createExcel)

        #update database button
        self.Updatedb = Button(self, text="Update db", command=self.updatedb)

        #option menu test
        self.variable = StringVar(self)
        self.variable.set(self.manufactureList[1])
        self.menu = OptionMenu(self, self.variable, *self.manufactureList)

        #pack widgets        
        self.CreateExcel.grid(row=0, column=2, padx=10, pady=10)
        self.Updatedb.grid(row=1, column=0, padx=10, pady=10)
        self.QUIT.grid(row=1, column=2, padx=10, pady=10)
        self.menu.grid(row=0, column=0, padx=10, pady=10)

    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.pack()
        self.compileDropdownList()
        self.createWidgets()

    #create an excel file for given manufacture
    def createExcel(self):
        dbc = SQLConnector.DatabaseConnection()        
        keyword = self.variable.get()
        
        xlw = excelWriting.ExcelBook(keyword)        
        xlw.populateTable(dbc.searchManufacture(keyword))
        xlw.close()
        

    #compile a manufacture list from the cms database
    def compileDropdownList(self):
        dbc = SQLConnector.DatabaseConnection()
        self.results = dbc.queryForManufactureList()
        self.manufactureList = []
        for each in self.results:
            self.manufactureList.append(each[1])
        self.manufactureList.sort()

    #update the database from the excelfile
    def updatedb(self):
        #get the selected manufacturer
        manufactureName = self.variable.get()
        #get the database info for the manucfaturer
        dbc = SQLConnector.DatabaseConnection()
        dbData = dbc.searchManufacture(manufactureName)
        
        #get the excek info for the manufacturer
        xlc = excelReader.ExcelBook()
        xlData = xlc.extractWorkbookData(manufactureName)
        
        #compare the data
        
        for rowNumber in range(0,len(xlData)):
            if (dbData[rowNumber] != tuple(xlData[rowNumber])):
                #The data does not match update database
                
                #print xlData[rowNumber]
                dbc.updateProduct(xlData[rowNumber])
            else:
                pass
                

        print "done"

root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()
