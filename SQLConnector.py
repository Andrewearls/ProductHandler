import MySQLdb
from excelWriting import ExcelBook

class DatabaseConnection():
    #connect to test database
    def connectTest(self):
        self.db = MySQLdb.connect(host="localhost",
                                  user="root",
                                  passwd="root",
                                  db="test_db")
        self.cur = self.db.cursor()
    
    #connect to new database
    def connectCleanData(self):
        self.db = MySQLdb.connect(host="localhost",
                             user="root",
                             passwd="root",
                             db="cleandata")
        self.cur = self.db.cursor()

    #connect to old database
    def connectCMS(self):
        self.db = MySQLdb.connect(host="localhost",
                                  user="root",
                                  passwd="root",
                                  db="cms")
        self.cur = self.db.cursor()
        
    #search database for manufacturer
    #send results to an excel file
    def searchManufacture(self, keyword='Quantum'):
        self.connectCleanData()
        self.keyword = keyword
        sqlQuery = 'SELECT * FROM raw_data WHERE manufactureName = "{}"'.format(keyword)
        
        self.cur.execute(sqlQuery)
        tableData = list(self.cur.fetchall())
        self.db.close()
        
        if not tableData:
            manufactureDetails = self.queryForManufactureList(keyword)
            print manufactureDetails
            #query old data for manufacturer
            self.insertProducts(self.extractProducts(*manufactureDetails[0]))
            #insert into new data
            #get data from new db
            tableData = self.searchManufacture(keyword)
        return tableData        

    #get the manufacturer names and ids
    def queryForManufactureList(self, manufactureName = None):
        self.connectCMS()
        if manufactureName == None:
            sqlQuery = 'SELECT manufactID, manufactName FROM manufacturer'
        else:
            sqlQuery = 'SELECT manufactID, manufactName FROM manufacturer WHERE manufactName = "{}"'.format(manufactureName)
            
        self.cur.execute(sqlQuery)
        results = self.cur.fetchall()
        self.db.close()
        return results

    #Extract products from old database
    def extractProducts(self, manufactureID, manufactureName):
        self.connectCMS()
        sqlQuery = \
"SELECT '{}' AS manufactureName, \
part.name AS modelNumber, \
MAX(part_attribute.attriValue) AS modelPrice, \
part_class.partClassName AS productName, \
part_category.partCatDesc AS productDescription, \
CONCAT('https://0c3e66699e7888fc796a-b81ff6485f85a81c17fc5ed8482993db.ssl.cf1.rackcdn.com/', \
part_class_images.imageFileName) AS imageLocation, \
CONCAT('https://materialflow.com/p/', part_class.seoName) AS URL \
FROM part \
JOIN part_attribute ON part.partID = part_attribute.partID \
LEFT JOIN part_class ON part.classID = part_class.classID \
LEFT JOIN part_class_images ON part.classID = part_class_images.parentID \
INNER JOIN part_class_link ON part_class.classID = part_class_link.classID \
INNER JOIN part_category ON part_class_link.partCatID = part_category.partCatID \
WHERE part.classID IN \
(SELECT part_class.classID \
FROM part_class \
WHERE part_class.manufactID = {}) \
AND part_attribute.attriValue LIKE '\$%' \
AND part_class_images.orderID = 1 \
AND part.InStock = 1 \
GROUP BY part.name;".format(manufactureName, int(manufactureID))
        self.cur.execute(sqlQuery)
        results = self.cur.fetchall()
        self.db.close()
        
        return results

    #insert clean data into new database
    def insertProducts(self, products):        
        self.connectCleanData()
        
        for i,each in enumerate(products):
            each = each + ("New", "In Stock",'Business & Industrial > Manufacturing')
            
            sqlQuery = "INSERT INTO raw_data (`manufactureName`,\
                                                `modelNumber`,\
                                                `modelPrice`,\
                                                `productName`,\
                                                `productDescription`,\
                                                `imageLocation`,\
                                                `URL`,\
                                                `productCondition`,\
                                                `availability`,\
                                                `googleProductCategory`) \
                        VALUES {};".format(each)
            try:
                self.cur.execute(sqlQuery)
                self.db.commit()
            except:
                self.db.rollback()
            
        self.db.close()

    def updateProduct(self, row):
        self.connectCleanData()
        rowID = row.pop(0)
        row.append(rowID)
        sqlQuery = 'UPDATE `raw_data` \
                    SET manufactureName = "{}",\
                        modelNumber = "{}",\
                        modelPrice = "{}",\
                        productName = "{}",\
                        productDescription = "{}",\
                        imageLocation = "{}",\
                        URL = "{}",\
                        productCondition = "{}",\
                        availability = "{}",\
                        googleProductCategory = "{}"\
                    WHERE ID = {};'.format(*row)
        try:
            self.cur.execute(sqlQuery)
            self.db.commit()
        except:
            self.db.rollback()
        self.db.close()



















        

