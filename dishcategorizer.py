from bs4 import BeautifulSoup;
import requests;
import re;
from openpyxl import load_workbook

#dishCategorizer does its best to categorize dishes so you don't have to. Right now I have it defaulting to Entree since that's what my lazy ass does, but I hope to refine it. Enjoy!
#Ones that are defaulted to "entree" will be "e". Those identified as entree will be "E". The Json converter will read them the same, this is just for proofreading.

    
def makeItRegEx(aList):
    regExList = []
    for word in aList:
        regExList.append("^"+word)
    return "|".join(regExList)


def appyCatcher(categoryName):
    categoryName = categoryName.lower()    
    appyWords = ["salad","salads","appetizer", "app", "small", "start", "share", "sharing","finger","insala", "bites", "soup", "soups"]
    appyWords = makeItRegEx(appyWords)
    isAppy = re.search(appyWords,categoryName)
    if isAppy:
        isAppy = True
        return isAppy
def entreeCatcher(categoryName):
    categoryName = categoryName.lower()
    entreeWords = ["Main", "burger", "veget", "vegan", "entree"]
    entreeWords = makeItRegEx(entreeWords)
    isEntree = re.search(entreeWords,categoryName)    
    return isEntree
def dessertCatcher(categoryName):
    categoryName = categoryName.lower()
    dessertWords = ["sweet","dessert"]
    dessertWords = makeItRegEx(dessertWords)
    isDessert = re.search(dessertWords,categoryName)    
    return isDessert    
def sideCatcher(categoryName):
    categoryName = categoryName.lower()
    sideWords = ["side","snack","a la carte","extra","bite"]
    sideWords = makeItRegEx(sideWords)
    isSide = re.search('r'+sideWords,categoryName)    
    return isSide    
def run(workbookName):
    workbook = load_workbook(filename = workbookName)    
    for worksheet in workbook:
        n=1 
        m=0
        while n<200:
            categoryName = worksheet['A'+str(n)].value
            
            if worksheet['A'+str(n)].value:
                pass
            else:
                worksheet['A'+str(n)].value = " "
            n=n+1
            
        n=2
        while n<200:
            categoryName = worksheet['A'+str(n)].value        
            if categoryName:
                if appyCatcher(categoryName):
                    worksheet['F'+str(n)] = "A"
                elif entreeCatcher(categoryName):
                    worksheet['F'+str(n)] = "E"
                elif dessertCatcher(categoryName):
                    worksheet["F"+str(n)]="D"
                elif sideCatcher(categoryName):
                    worksheet["F"+str(n)]="S"
                elif categoryName == "Category":
                    worksheet["F" + str(n)] = "Type"
                elif categoryName != " ":
                    try:
                        worksheet["F"+str(n)]="e"
                    except:
                        pass
            
    
            n+=1
            m+=1
    try:
        
        address = getAddress(worksheet['B1'].value)
        worksheet['G3'] = address[0]
        worksheet['G4'] = address[1]
    except: 
        pass
    
    workbook.save(workbookName)
    workbook.close()
    
def getAddress(address):
    url = address
    content = requests.get(url).content
    print(url)
    print(content)
    soup = BeautifulSoup(content,"html.parser");    
    address = soup.find(class_="vendor-location").string
    address = address.split(',')
    return address

#sheet_ranges = wb['range names']
#print(sheet_ranges['D18'].value)