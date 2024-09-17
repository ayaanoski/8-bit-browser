import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QWidget,
    QLabel,
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QUrl, QSize


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window properties
        self.setWindowTitle("8-Bit Retro Browser")
        self.setWindowIcon(
            QIcon(
                "E:\\web\\images\\logo.png"
            )  # Replace with your application icon path
        )
        self.setGeometry(100, 100, 800, 600)

        # Create the web view for displaying web pages
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))

        # Connect the `loadFinished` signal to the 8-bit style injection function
        self.browser.loadFinished.connect(self.apply_8bit_style)

        # Create the navigation bar components
        self.url_bar = QLineEdit()
        self.url_bar.setFont(QFont("Press Start 2P", 10))
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        # Create navigation buttons with images
        button_size = QSize(30, 30)  # Reduced button size

        back_btn = QPushButton()
        back_btn.setIcon(
            QIcon(
                "E:\\web\\images\\back.png"
            )  # Replace with your back button image path
        )
        back_btn.setFixedSize(button_size)
        back_btn.clicked.connect(self.browser.back)

        forward_btn = QPushButton()
        forward_btn.setIcon(
            QIcon(
                "E:\\web\\images\\next.png"
            )  # Replace with your forward button image path
        )
        forward_btn.setFixedSize(button_size)
        forward_btn.clicked.connect(self.browser.forward)

        refresh_btn = QPushButton()
        refresh_btn.setIcon(
            QIcon(
                "E:\\web\\images\\undo.png"
            )  # Replace with your refresh button image path
        )
        refresh_btn.setFixedSize(button_size)
        refresh_btn.clicked.connect(self.browser.reload)

        home_btn = QPushButton()
        home_btn.setIcon(
            QIcon(
                "E:\\web\\images\\home.png"
            )  # Replace with your home button image path
        )
        home_btn.setFixedSize(button_size)
        home_btn.clicked.connect(self.navigate_home)

        # Optional: Set icon sizes explicitly (if needed)
        back_btn.setIconSize(QSize(20, 20))  # Reduced icon size
        forward_btn.setIconSize(QSize(20, 20))
        refresh_btn.setIconSize(QSize(20, 20))
        home_btn.setIconSize(QSize(20, 20))

        logo_label = QLabel()
        logo_label.setPixmap(
            QIcon("E:\\web\\images\\logo.png").pixmap(60, 60)  # Reduced logo size
        )

        # Create a horizontal layout for the navigation bar
        nav_layout = QHBoxLayout()
        nav_layout.setContentsMargins(5, 5, 5, 5)
        nav_layout.setSpacing(5)

        nav_layout.addWidget(back_btn)
        nav_layout.addWidget(forward_btn)
        nav_layout.addWidget(refresh_btn)
        nav_layout.addWidget(home_btn)
        nav_layout.addWidget(self.url_bar)
        nav_layout.addWidget(logo_label)

        nav_widget = QWidget()
        nav_widget.setLayout(nav_layout)

        # Set a fixed height for the navigation bar (this is the key part)
        nav_widget.setFixedHeight(70)  # Adjust this value as needed for a normal height

        main_layout = QVBoxLayout()
        main_layout.addWidget(nav_widget)
        main_layout.addWidget(self.browser)

        widget = QWidget()
        widget.setLayout(main_layout)

        self.setCentralWidget(widget)

        self.setStyleSheet(
            """
            QWidget {
                font-family: "Press Start 2P", cursive;
                background-color: #000;
                color: #0f0;
            }

            QPushButton {
                background-color: #444;
                border: 2px solid #0f0;
                color: #fff;
                border-radius: 5px;  /* Rounded corners */
                padding: 0;  /* Reduced padding */
            }

            QLineEdit {
                background-color: #111;
                border: 2px solid orange;
                color: #0f0;
                height: 30px;  /* Reduced height */
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

    def apply_8bit_style(self):
        current_url = self.browser.url().toString()

        # General 8-bit style for all pages
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

        # Apply dark mode and custom logo only if it's the Google homepage
        if current_url in ["https://www.google.com/", "https://www.google.com/?hl=en"]:
            google_css = """
            body, html {
                background-color: #000 !important;
                color: #0f0 !important;
            }
            a {
                color: #0f0 !important;
            }
            input {
                background-color: #111 !important;
                border: 2px solid #0f0 !important;
                color: #0f0 !important;
            }
            """

            google_js_code = f"""
            (function() {{
                // Replace the logo
                var logo = document.querySelector('img[alt="Google"]');
                if (logo) {{
                    logo.src = 'https://www.pikpng.com/pngl/b/60-607449_pixelated-google-logo-google-logo-pixel-art-clipart.png';  // Replace with your custom logo URL
                    logo.srcset = '';
                }}
            }})();
            """
            js_code += google_js_code

        # Inject JavaScript to apply styles
        self.browser.page().runJavaScript(
            js_code, lambda _: print("8-bit style applied")
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Press Start 2P", 10))

    window = Browser()
    window.showMaximized()

    sys.exit(app.exec_())
