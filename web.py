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
from PyQt5.QtCore import QUrl, QSize, Qt, QPoint


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        # Get the absolute path of the script directory
        self.script_dir = os.path.dirname(os.path.abspath(__file__))

        # Remove default window decorations (including title bar)
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Set up the main window properties
        self.setWindowTitle("8-Bit Retro Browser")
        self.setWindowIcon(QIcon(os.path.join(self.script_dir, "images", "logo.png")))
        self.setGeometry(100, 100, 800, 600)

        # Custom Title Bar
        self.title_bar = QWidget(self)
        self.title_bar.setFixedHeight(40)
        self.title_bar.setStyleSheet(
            """
            background-color: black;
            color: green;
            font-family: "Press Start 2P";
            border-bottom: 2px solid #0f0;
            """
        )

        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(5, 0, 5, 0)

        # Title label
        title_label = QLabel("8-Bit Retro Browser")
        title_label.setStyleSheet("color: green;")
        title_layout.addWidget(title_label)

        title_layout.addStretch()  # Stretch to push the title to the left

        # Create custom minimize, maximize/restore, and close buttons
        minimize_btn = QPushButton("_")
        maximize_btn = QPushButton("☐")
        close_btn = QPushButton("X")

        for btn in [minimize_btn, maximize_btn, close_btn]:
            btn.setFixedSize(30, 30)
            btn.setStyleSheet(
                """
                QPushButton {
                    background-color: black;
                    color: green;
                    border: 2px solid #0f0;
                    font-family: "Press Start 2P";
                }
                QPushButton:hover {
                    background-color: #111;
                }
                """
            )

        minimize_btn.clicked.connect(self.showMinimized)
        maximize_btn.clicked.connect(self.toggle_maximize)
        close_btn.clicked.connect(self.close)

        title_layout.addWidget(minimize_btn)
        title_layout.addWidget(maximize_btn)
        title_layout.addWidget(close_btn)

        # Drag functionality for the custom title bar
        self.old_position = None
        self.title_bar.mousePressEvent = self.mouse_press_event
        self.title_bar.mouseMoveEvent = self.mouse_move_event

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

        # Add navigation buttons first
        nav_layout.addWidget(back_btn)
        nav_layout.addWidget(forward_btn)
        nav_layout.addWidget(refresh_btn)
        nav_layout.addWidget(home_btn)

        # Add the url_bar next
        nav_layout.addWidget(self.url_bar)

        # Move bookmark and inspect buttons after url_bar
        nav_layout.addWidget(bookmark_btn)
        nav_layout.addWidget(inspect_btn)

        # Add logo label last
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

        # Add title bar at the top
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.title_bar)  # Add title bar first
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

                # Add a bookmark button to the bookmark bar
                bookmark_button = QPushButton(bookmark_name)
                bookmark_button.setFixedHeight(20)  # Reduce bookmark button height
                bookmark_button.setStyleSheet(
                    """
                    QPushButton {
                        background-color: #fff;
                        color: #000;
                        border: 2px solid #0f0;
                    }
                    """
                )
                bookmark_button.clicked.connect(
                    lambda: self.browser.setUrl(QUrl(current_url))
                )
                self.bookmark_bar_layout.addWidget(bookmark_button)
            else:
                QMessageBox.warning(
                    self,
                    "Duplicate Bookmark",
                    "This bookmark already exists in the bookmark bar.",
                )

    def toggle_dev_tools(self):
        if self.dev_dock.isVisible():
            self.dev_dock.hide()
        else:
            self.dev_dock.show()

    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def mouse_press_event(self, event):
        if event.button() == Qt.LeftButton:
            self.old_position = event.globalPos()

    def mouse_move_event(self, event):
        if event.buttons() == Qt.LeftButton:
            delta = QPoint(event.globalPos() - self.old_position)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_position = event.globalPos()

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


def main():
    app = QApplication(sys.argv)
    browser = Browser()
    browser.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
