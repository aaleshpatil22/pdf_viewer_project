# NOTES 

### what I want to accomplish? 
1. PDF preview
2. based on UI filter on PyQT the PDF preview must be updated
3. data to be showed on PDF report is taken from SQLite database


### How I want to accomplish the above?
1. test pdf preview required
2. test to show UI field from sqlite
3. show report with updated data from fields selected above and previewed on PDF


# BEGIN 

### PDF PREVIEW TEST
1. PyQT webview can display the PDF https://stackoverflow.com/questions/23389001/how-to-render-pdf-using-pdf-js-viewer-in-pyqt
2. done with right {{'url': '{file_url}'}}


### DATA FILTERING TO SQLITE 
1. date filtering using calendar ui https://github.com/baoboa/pyqt5/blob/master/examples/widgets/calendarwidget.py
2. used colnRpt and readymade PyQt5 Ui which works but does not have QtWebView ready


### DATA FILTER AND REPORT PDF RENDER 
1. Combine above two 

# ADDITIONAL 

### CREATE WORKING INSTALLER WITH ALL WIDGETS 
1. something related to paths where each widget is mentioned and picked up independently 
2. also add config for database path 
3. add logging 


# PREREQUISITES
1. setup venv 
2. install required libraries - PyQt5 and fbs
3. install https://build-system.fman.io/qt-designer-download
4. PySide6 works better and comes with QtWebView installed
5. 