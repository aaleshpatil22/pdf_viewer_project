import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QMenu, QMenuBar, QFileDialog
from PySide6.QtCore import QUrl
from PySide6.QtGui import QAction, QIcon, QPixmap
from PySide6.QtWebEngineWidgets import QWebEngineView

class PdfViewerWidget(QWidget):

    def __init__(self, pdfjs_path):
        super().__init__()

        layout = QVBoxLayout(self)

        self.webview = QWebEngineView()
        local_url = QUrl.fromLocalFile(pdfjs_path).toString()
        self.webview.load(QUrl(local_url))

        layout.addWidget(self.webview)

        def on_load_finished(ok):
            if ok and self.pdf_file:
                file_url = QUrl.fromLocalFile(self.pdf_file).toString()
                self.webview.page().runJavaScript(
                    f"PDFViewerApplication.open({{'url': '{file_url}'}});"
                )

        self.webview.loadFinished.connect(on_load_finished)

        self.pdf_file = None

    def open_pdf(self):
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Open PDF File")
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("PDF Files (*.pdf)")

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
        my_pixmap = QPixmap(Path("E:\projects\MultiReportwithDB\1pdfviewer\icon.png"))
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
    pdfjs_path = str(Path.home() / 'js' / 'pdfjs' / 'web' / 'viewer.html')

    main_win = PdfViewerApp(pdfjs_path)
    main_win.show()

    sys.exit(app.exec())