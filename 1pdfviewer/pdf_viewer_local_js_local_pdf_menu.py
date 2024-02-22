import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QFileDialog, QLabel,QComboBox,QDateEdit,QGridLayout,QPushButton,QSizePolicy
from PySide6.QtCore import QUrl
from PySide6.QtGui import QAction, QIcon, QPixmap
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import Qt, QDate
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import duckdb

class PdfViewerWidget(QWidget):

    def __init__(self, pdfjs_path):
        super().__init__()

        layout = QVBoxLayout(self)
        hlayout = QGridLayout(self)
        
        self.sales_group_label = QLabel("Sales Group")
        self.sales_group_box = QComboBox(self)
        self.sales_group_box.addItems(['Dairy-1', 'Dairy-2', 'Dairy-3', 'Dairy-4', 'Dairy-5'])
        
        self.from_date_label = QLabel("From:")
        self.from_date_input = QDateEdit(self)
        self.from_date_input.setDate(QDate.currentDate())
        
        self.to_date_label = QLabel("To:")
        self.to_date_input = QDateEdit(self)
        self.to_date_input.setDate(QDate.currentDate())
        
        self.item_group_label = QLabel("Item Group")
        self.item_group_box = QComboBox(self)
        self.item_group_box.addItems(['milk', 'butter', 'ghee', 'cheese', 'paneer'])
        
        self.option_group_label = QLabel("Option Group")
        self.option_group_box = QComboBox(self)
        self.option_group_box.addItems(['milk', 'butter', 'ghee', 'cheese', 'paneer'])
        
        self.show_button = QPushButton("Show")
        self.show_button.clicked.connect(self.show)
        self.show_button.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Expanding)
        
        hlayout.addWidget(self.sales_group_label,0,0,1,1)
        hlayout.addWidget(self.sales_group_box,0,1,1,2)
        
        hlayout.addWidget(self.from_date_label,0,3,1,1)
        hlayout.addWidget(self.from_date_input,0,4,1,1)
        hlayout.addWidget(self.to_date_label,0,5,1,1)
        hlayout.addWidget(self.to_date_input,0,6,1,1)
        
        hlayout.addWidget(self.item_group_label,1,0,1,1)
        hlayout.addWidget(self.item_group_box,1,1,1,3)
        hlayout.addWidget(self.option_group_label,1,4,1,1)
        hlayout.addWidget(self.option_group_box,1,5,1,3)
        hlayout.addWidget(self.show_button,0,8,2,1)
        
        self.webview = QWebEngineView()
        local_url = QUrl.fromLocalFile(pdfjs_path).toString()
        self.webview.load(QUrl(local_url))

        layout.addLayout(hlayout)
        layout.addWidget(self.webview)

        def on_load_finished(ok):
            if ok and self.pdf_file:
                file_url = QUrl.fromLocalFile(self.pdf_file).toString()
                self.webview.page().runJavaScript(
                    f"PDFViewerApplication.open({{'url': '{file_url}'}});"
                )

        self.webview.loadFinished.connect(on_load_finished)

        self.pdf_file = None
        
    def show(self):
        
        self.from_date = self.from_date_input.date().toString(Qt.ISODate)
        self.to_date = self.to_date_input.date().toString(Qt.ISODate)
        #self.from_date = '2024-02-21'
        #self.to_date = '2024-02-23'
        
        db_file_path = 'example_database.db'
        # Establish a connection to DuckDB and create a disk-based database
        connection = duckdb.connect(database=db_file_path, read_only=False)

        # Execute a query to fetch data from the table (just for verification)
        #query_result = connection.execute(f"select * from dairy where date between {self.from_date_input.date().toString(Qt.ISODate)} and {self.from_date_input.date().toString(Qt.ISODate)}")
        query_result = connection.execute(f"select * from dairy where date between '{self.from_date}' and '{self.to_date}'")
        rows = query_result.fetchall()
        # Get the column names from the query result description
        columns = [column[0] for column in query_result.description]
        # Create a DataFrame using the fetched rows and column names
        df_result = pd.DataFrame(rows, columns=columns)
        
        plt.figure(figsize=(8, 6))
        plt.text(0.5, 0.95, 'ERP SOLUTIONS Pvt. Ltd.', fontsize=18, ha='center', va='center')
        
        plt.text(0.5, 0.9, f"From Date {self.from_date_input.date().toString(Qt.ISODate)} To {self.to_date_input.date().toString(Qt.ISODate)}", fontsize=8, ha='center', va='center')
        
        plt.text(0.5, 0.85, f"Stock Statement Report For {self.sales_group_box.currentText()} Option {self.option_group_box.currentText()}", fontsize=8, ha='center', va='center')
        
        plt.text(0.1, 0.8, f"Print Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", fontsize=8, ha='center', va='center')
        
        plt.table(cellText=df_result.values,
            colLabels=df_result.columns,
            cellLoc='center',
            loc='center')
       
        # Replace 'output_file.pdf' with your desired output file name
        plt.axis('off')
        
        path = Path.home() / 'pdfjs' / 'web' / 'doc' / f'{datetime.now().strftime("%d%m%Y%H%M%S")}.pdf'
        
        plt.savefig(path, format='pdf')
        self.pdf_file = path
        self.webview.reload()
        
        #plt.show()

    def open_pdf(self):
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Open PDF File")
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("PDF Files (*.pdf)")
        path1 = str(Path.home() / 'pdfjs' / 'web'/ 'doc')
        file_dialog.setDirectory(path1)
        

        if file_dialog.exec_() == QFileDialog.Accepted:
            self.pdf_file = file_dialog.selectedFiles()[0]
            self.webview.reload()

class PdfViewerApp(QMainWindow):

    def __init__(self, pdfjs_path):
        super().__init__()

        self.viewer = PdfViewerWidget(pdfjs_path)
        self.setCentralWidget(self.viewer)

        self.create_menu_bar()

        # Set the title and icon
        self.setWindowTitle("PDF Viewer App")
        my_pixmap = QPixmap(Path("icon.png"))
        self.setWindowIcon(QIcon(my_pixmap))

    def create_menu_bar(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")

        open_action = QAction("Open PDF...", self)
        open_action.triggered.connect(self.viewer.open_pdf)
        file_menu.addAction(open_action)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Make sure you replace this path with the path to your local PDF.js 'viewer.html' file
    #pdfjs_path = "C:/Users/Aalesh/PycharmProjects/chetan_project/pdf_viewer_project/Resources/pdfjs/web/viewer.html"
    pdfjs_path = Path.home() / 'pdfjs' / 'web' / 'viewer.html'
    main_win = PdfViewerApp(pdfjs_path)
    main_win.show()

    sys.exit(app.exec())