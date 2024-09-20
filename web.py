import sys
import os
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QWidget,
    QLabel,
    QMessageBox,
    QDockWidget,
    QInputDialog,
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QUrl, QSize, Qt


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        # Get the absolute path of the script directory
        self.script_dir = os.path.dirname(os.path.abspath(__file__))

        # Set up the main window properties
        self.setWindowTitle("8-Bit Retro Browser")
        self.setWindowIcon(
            QIcon(os.path.join(self.script_dir, "images", "logo.png"))
        )  # Use relative path for application icon
        self.setGeometry(100, 100, 800, 600)

        # Create the web view for displaying web pages
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))

        # Create developer tools window (QDockWidget)
        self.dev_tools = QWebEngineView()
        self.dev_dock = QDockWidget("Developer Tools", self)
        self.dev_dock.setWidget(self.dev_tools)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dev_dock)
        self.dev_dock.hide()

        # Set the page for the main browser and connect developer tools to it
        self.browser.page().setDevToolsPage(self.dev_tools.page())

        # Connect the `loadFinished` signal to the 8-bit style injection function
        self.browser.loadFinished.connect(self.apply_8bit_style)

        # Create the navigation bar components
        self.url_bar = QLineEdit()
        self.url_bar.setFont(QFont("Press Start 2P", 10))
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        # Create navigation buttons with images using relative paths
        button_size = QSize(30, 30)  # Reduced button size

        back_btn = QPushButton()
        back_btn.setIcon(QIcon(os.path.join(self.script_dir, "images", "back.png")))
        back_btn.setFixedSize(button_size)
        back_btn.clicked.connect(self.browser.back)

        forward_btn = QPushButton()
        forward_btn.setIcon(QIcon(os.path.join(self.script_dir, "images", "next.png")))
        forward_btn.setFixedSize(button_size)
        forward_btn.clicked.connect(self.browser.forward)

        refresh_btn = QPushButton()
        refresh_btn.setIcon(QIcon(os.path.join(self.script_dir, "images", "undo.png")))
        refresh_btn.setFixedSize(button_size)
        refresh_btn.clicked.connect(self.browser.reload)

        home_btn = QPushButton()
        home_btn.setIcon(QIcon(os.path.join(self.script_dir, "images", "home.png")))
        home_btn.setFixedSize(button_size)
        home_btn.clicked.connect(self.navigate_home)

        bookmark_btn = QPushButton()
        bookmark_btn.setIcon(
            QIcon(os.path.join(self.script_dir, "images", "heart.png"))
        )
        bookmark_btn.setFixedSize(button_size)
        bookmark_btn.clicked.connect(self.add_bookmark)

        inspect_btn = QPushButton()
        inspect_btn.setIcon(
            QIcon(os.path.join(self.script_dir, "images", "inspect.png"))
        )
        inspect_btn.setFixedSize(button_size)
        inspect_btn.clicked.connect(self.toggle_dev_tools)

        logo_label = QLabel()
        logo_label.setPixmap(
            QIcon(os.path.join(self.script_dir, "images", "logo.png")).pixmap(60, 60)
        )

        # Create a horizontal layout for the navigation bar
        nav_layout = QHBoxLayout()
        nav_layout.setContentsMargins(5, 5, 5, 5)
        nav_layout.setSpacing(5)

        nav_layout.addWidget(back_btn)
        nav_layout.addWidget(forward_btn)
        nav_layout.addWidget(refresh_btn)
        nav_layout.addWidget(home_btn)
        nav_layout.addWidget(bookmark_btn)
        nav_layout.addWidget(inspect_btn)
        nav_layout.addWidget(self.url_bar)
        nav_layout.addWidget(logo_label)

        nav_widget = QWidget()
        nav_widget.setLayout(nav_layout)

        # Set a fixed height for the navigation bar
        nav_widget.setFixedHeight(70)

        # Create a horizontal layout for the bookmark bar
        self.bookmark_bar_layout = QHBoxLayout()
        self.bookmark_bar_layout.setContentsMargins(5, 0, 5, 0)
        self.bookmark_bar_layout.setSpacing(5)

        bookmark_bar_widget = QWidget()
        bookmark_bar_widget.setLayout(self.bookmark_bar_layout)
        bookmark_bar_widget.setFixedHeight(30)  # Very thin bookmark bar

        main_layout = QVBoxLayout()
        main_layout.addWidget(nav_widget)
        main_layout.addWidget(bookmark_bar_widget)  # Add bookmark bar just below navbar
        main_layout.addWidget(self.browser)

        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

        # Bookmark storage (bookmark name and URL)
        self.bookmarks = []

        # Updated style sheet for button sizes and colors
        self.setStyleSheet(
            """
    QWidget {
        font-family: "Press Start 2P", cursive;
        background-color: #000;  /* Background color black */
        color: #0f0;  /* Green text */
    }

    QPushButton {
        background-color: gray;  /* Button color black */
        border: 2px solid #0f0;  /* Green border */
        color: #fff;  /* White text */
        border-radius: 5px;
        padding: 0px;  /* Adjust padding */
    }

    QLineEdit {
        background-color: #111;  /* Darker input field background */
        border: 2px solid #0f0;  /* Green border */
        color: #0f0;  /* Green text */
        height: 30px;  /* Fixed height */
    }

    QPushButton#bookmark_bar QPushButton {
        font-size: 10px;
        min-width: 100px;
        max-width: 200px;
        padding: 10px;
        color: #000;  /* Black text */
        background-color: #fff;  /* White background */
    }
    """
        )

    def navigate_to_url(self):
        url = self.url_bar.text().strip()

        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://www.google.com/search?q=" + url

        self.browser.setUrl(QUrl(url))

    def navigate_home(self):
        self.browser.setUrl(QUrl("https://www.google.com"))

    def add_bookmark(self):
        current_url = self.browser.url().toString()

        # Prompt user for bookmark name
        bookmark_name, ok = QInputDialog.getText(
            self,
            "Bookmark Name",
            "Enter a name for the bookmark:",
            flags=Qt.Dialog | Qt.WindowTitleHint | Qt.CustomizeWindowHint,
        )

        if ok and bookmark_name:
            # Check if the bookmark already exists
            if not any(bm["url"] == current_url for bm in self.bookmarks):
                self.bookmarks.append({"name": bookmark_name, "url": current_url})

                # Create a new button for the bookmark with increased size
                bookmark_btn = QPushButton(bookmark_name)
                bookmark_btn.setStyleSheet(
                    """
                    font-size: 12px;  /* Increased font size */
                    color: #000;
                    background-color: white;
                    border: 2px solid #0f0;
                    padding: 5px;     /* Padding for larger button */
                    min-width: 120px;  /* Minimum width for better visibility */
                    max-width: 200px;  /* Maximum width */
                    min-height: 20px;  /* Minimum height for better visibility */
                    max-height: 30px;  /* Maximum height */
                    """
                )

                # Connect button click to navigate to URL
                bookmark_btn.clicked.connect(
                    lambda url=current_url: self.browser.setUrl(QUrl(url))
                )

                # Add button to the layout
                self.bookmark_bar_layout.addWidget(bookmark_btn)

                # Show confirmation message
                msg_box = QMessageBox(self)
                msg_box.setWindowFlags(
                    Qt.Dialog | Qt.WindowTitleHint | Qt.CustomizeWindowHint
                )
                msg_box.information(
                    self,
                    "Bookmark Added",
                    f"'{bookmark_name}' has been added to bookmarks.",
                )
            else:
                msg_box = QMessageBox(self)
                msg_box.setWindowFlags(
                    Qt.Dialog | Qt.WindowTitleHint | Qt.CustomizeWindowHint
                )
                msg_box.warning(
                    self, "Bookmark Exists", f"'{current_url}' is already in bookmarks."
                )

    def toggle_dev_tools(self):
        if self.dev_dock.isVisible():
            self.dev_dock.hide()
        else:
            self.dev_dock.show()

    def apply_8bit_style(self):
        css = """
        body, html, * {
            image-rendering: crisp-edges !important;
            font-family: "Press Start 2P", cursive !important;
            filter: contrast(110%) brightness(98%) !important;
            letter-spacing: 1px;
        }

        img {
            image-rendering: pixelated !important;
            filter: contrast(110%) brightness(110%);
        }
        """

        js_code = f"""
        (function() {{
            var style = document.createElement('style');
            style.type = 'text/css';
            style.innerHTML = `{css}`;
            document.head.appendChild(style);
        }})();

        """

        self.browser.page().runJavaScript(
            js_code, lambda _: print("8-bit style applied")
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Press Start 2P", 10))

    window = Browser()
    window.showMaximized()

    sys.exit(app.exec_())
