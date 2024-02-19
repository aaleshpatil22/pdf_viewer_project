import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtCore import QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PySide6.QtWebEngineWidgets import QWebEngineView

class PdfViewerWidget(QWidget):

    def __init__(self, pdfjs_path, pdf_file):
        super().__init__()
        
        layout = QVBoxLayout(self)
        
        self.webview = QWebEngineView()
        local_url = QUrl.fromLocalFile(pdfjs_path).toString()
        self.webview.load(QUrl(local_url))
        
        layout.addWidget(self.webview)
        
        def on_load_finished(ok):
            if ok:
                file_url = QUrl.fromLocalFile(pdf_file).toString()
                self.webview.page().runJavaScript(
                    f"PDFViewerApplication.open({{'url': '{file_url}'}});"
                )
                
        self.webview.loadFinished.connect(on_load_finished)

if __name__ == "__main__":

    app = QApplication(sys.argv)
    # Make sure you replace this path with the path to your local PDF.js 'viewer.html' file
    pdfjs_path = Path.home() / 'js' / 'pdfjs' / 'web' / 'viewer.html'

    # The path to the PDF file you want to open
    pdf_file = Path.home() / 'Documents' / 'collection_report.pdf'

    viewer = PdfViewerWidget(pdfjs_path, pdf_file)
    viewer.show()
    
    sys.exit(app.exec())