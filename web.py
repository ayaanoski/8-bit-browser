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
    QTabWidget,
    QMenu,
)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QUrl, QSize, Qt, QPoint
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QSlider
from PyQt5.QtMultimedia import QMediaPlaylist
from PyQt5.QtWebEngineWidgets import QWebEngineSettings
from PyQt5.QtWebEngineWidgets import QWebEngineProfile


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        # Get the absolute path of the script directory
        self.script_dir = os.path.dirname(os.path.abspath(__file__))

        # Remove default window decorations (including title bar)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.set_web_engine_settings()

        # Set up the main window properties
        self.setWindowTitle("OR-BIT")
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
        title_label = QLabel("OR-BIT")
        title_label.setStyleSheet("color: #0f0;")
        title_layout.addWidget(title_label)

        title_layout.addStretch()

        # Create custom minimize, maximize/restore, and close buttons
        minimize_btn = QPushButton("_")
        maximize_btn = QPushButton("☐")
        close_btn = QPushButton("❌")

        for btn in [minimize_btn, maximize_btn, close_btn]:
            btn.setFixedSize(30, 30)
            btn.setStyleSheet(
                """
                QPushButton {
                    background-color: gray;
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

        # Tab widget for multiple tabs
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.currentChanged.connect(self.update_url_bar)

        # Add "+" tab for adding new tabs
        self.add_new_tab_button()

        # Create developer tools window (QDockWidget)
        self.dev_tools_view = QWebEngineView()
        self.dev_dock = QDockWidget("Developer Tools", self)
        self.dev_dock.setWidget(self.dev_tools_view)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dev_dock)
        self.dev_dock.hide()

        # Create the navigation bar components
        self.url_bar = QLineEdit()
        self.url_bar.setFont(QFont("Press Start 2P", 10))
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        button_size = QSize(30, 30)

        back_btn = QPushButton()
        back_btn.setIcon(QIcon(os.path.join(self.script_dir, "images", "back.png")))
        back_btn.setFixedSize(button_size)
        back_btn.clicked.connect(self.browser_back)

        forward_btn = QPushButton()
        forward_btn.setIcon(QIcon(os.path.join(self.script_dir, "images", "next.png")))
        forward_btn.setFixedSize(button_size)
        forward_btn.clicked.connect(self.browser_forward)

        refresh_btn = QPushButton()
        refresh_btn.setIcon(QIcon(os.path.join(self.script_dir, "images", "undo.png")))
        refresh_btn.setFixedSize(button_size)
        refresh_btn.clicked.connect(self.browser_refresh)

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
        self.bookmark_bar_layout = QHBoxLayout()
        self.bookmark_bar_layout.setContentsMargins(5, 0, 5, 0)
        self.bookmark_bar_layout.setSpacing(5)

        bookmark_bar_widget = QWidget()
        bookmark_bar_widget.setLayout(self.bookmark_bar_layout)
        bookmark_bar_widget.setFixedHeight(30)  # Very thin bookmark bar
        # Volume control slider
        volume_slider = QSlider(Qt.Horizontal)
        volume_slider.setRange(0, 100)  # Range from 0 to 100 (volume percentage)
        volume_slider.setValue(50)  # Default value (50% volume)
        volume_slider.setFixedWidth(100)
        volume_slider.valueChanged.connect(self.set_volume)

        nav_layout = QHBoxLayout()
        nav_layout.setContentsMargins(5, 5, 5, 5)
        nav_layout.setSpacing(5)

        nav_layout.addWidget(back_btn)
        nav_layout.addWidget(forward_btn)
        nav_layout.addWidget(refresh_btn)
        nav_layout.addWidget(home_btn)
        nav_layout.addWidget(self.url_bar)
        nav_layout.addWidget(bookmark_btn)
        nav_layout.addWidget(inspect_btn)
        nav_layout.addWidget(QLabel("Volume"))  # Add a label for the volume slider
        nav_layout.addWidget(volume_slider)
        nav_layout.addWidget(logo_label)

        nav_widget = QWidget()
        nav_widget.setLayout(nav_layout)
        nav_widget.setFixedHeight(70)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.title_bar)

        main_layout.addWidget(nav_widget)
        main_layout.addWidget(bookmark_bar_widget)
        main_layout.addWidget(self.tab_widget)

        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)
        self.music_player = QMediaPlayer()
        self.load_background_music()
        self.bookmarks = []

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
        QPushButton:hover {
                    background-color: #111;
                }

        QLineEdit {
            background-color: #111;  /* Darker input field background */
            border: 2px solid #0f0;  /* Green border */
            color: #0f0;  /* Green text */
            height: 30px;  /* Fixed height */
        }

         QTabWidget::pane { border: 2px solid #0f0; }
            QTabWidget::tab-bar { left: 10px; }

            QTabBar::tab {
                background-color: #000;
                color: #0f0;
                padding: 10px;
                margin-right: 5px;  /* Space between tabs */
                border-right: 1px solid #0f0;  /* Right border for separation */
            }

            QTabBar::tab:selected { background-color: #111; }
            QTabBar::tab:last { border-right: none; }  /* Remove right border from the last tab */

        """
        )

        # Open the initial tab with the home page
        self.add_new_tab(QUrl("https://www.google.com"), "Home")

    def set_web_engine_settings(self):
        profile = QWebEngineProfile.defaultProfile()
        profile.setRequestInterceptor(None)

        # Disable GPU acceleration
        profile.setPersistentStoragePath(os.path.join(self.script_dir, "webengine"))
        profile.setCachePath(os.path.join(self.script_dir, "webengine_cache"))
        profile.setPersistentStoragePath(
            os.path.join(self.script_dir, "webengine_persistent")
        )

        # Set other WebEngine settings
        QWebEngineSettings.globalSettings().setAttribute(
            QWebEngineSettings.AutoLoadImages, True
        )
        QWebEngineSettings.globalSettings().setAttribute(
            QWebEngineSettings.JavascriptEnabled, True
        )
        QWebEngineSettings.globalSettings().setAttribute(
            QWebEngineSettings.LocalStorageEnabled, True
        )
        QWebEngineSettings.globalSettings().setAttribute(
            QWebEngineSettings.WebRTCPublicInterfacesOnly, False
        )

    def add_new_tab(self, qurl=None, label="New Tab"):
        if qurl is None:
            qurl = QUrl("https://www.google.com")

        browser = QWebEngineView()
        browser.setUrl(qurl)

        # Set up developer tools for the browser
        browser.page().setDevToolsPage(self.dev_tools_view.page())

        # Update the tab label when the URL changes
        browser.titleChanged.connect(
            lambda title: self.tab_widget.setTabText(
                self.tab_widget.currentIndex(), title if title else "Untitled"
            )
        )

        browser.urlChanged.connect(lambda q: self.update_url_bar())
        browser.loadFinished.connect(lambda success: self.apply_8bit_style(browser))

        index = self.tab_widget.insertTab(self.tab_widget.count() - 1, browser, label)
        self.tab_widget.setCurrentIndex(index)

    def close_tab(self, index):
        if self.tab_widget.count() > 1:
            self.tab_widget.removeTab(index)
        else:
            self.close()

    def apply_8bit_style(self, browser):
        # Inject 8-bit style CSS
        browser.page().runJavaScript(
            """
            var css = `
            * {
                font-family: "Press Start 2P", cursive !important;
            }
            `;
            var style = document.createElement('style');
            style.innerHTML = css;
            document.head.appendChild(style);
            """
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

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "http://" + url
        self.tab_widget.currentWidget().setUrl(QUrl(url))

    def navigate_home(self):
        self.tab_widget.currentWidget().setUrl(QUrl("https://www.google.com"))

    def update_url_bar(self):
        current_browser = self.tab_widget.currentWidget()
        if isinstance(current_browser, QWebEngineView):
            self.url_bar.setText(current_browser.url().toString())

    def browser_back(self):
        current_browser = self.tab_widget.currentWidget()
        if isinstance(current_browser, QWebEngineView):
            current_browser.back()

    def browser_forward(self):
        current_browser = self.tab_widget.currentWidget()
        if isinstance(current_browser, QWebEngineView):
            current_browser.forward()

    def browser_refresh(self):
        current_browser = self.tab_widget.currentWidget()
        if isinstance(current_browser, QWebEngineView):
            current_browser.reload()

    def add_new_tab_button(self):
        new_tab_btn = QPushButton("+")
        new_tab_btn.setFixedSize(30, 30)
        # Adjust the button's position by adding a top margin
        new_tab_btn.setStyleSheet(
            "margin-top: 5px; margin-bottom: 9px;"
        )  # Negative top margin to move it up
        new_tab_btn.clicked.connect(lambda: self.add_new_tab())
        self.tab_widget.setCornerWidget(new_tab_btn, Qt.TopLeftCorner)

    def add_bookmark(self):
        current_browser = self.tab_widget.currentWidget()
        if isinstance(current_browser, QWebEngineView):
            url = current_browser.url().toString()

            # Create a custom input dialog for bookmark title
            dialog = QInputDialog(self)
            dialog.setWindowFlags(
                Qt.FramelessWindowHint | Qt.Popup
            )  # Remove title bar, make it popup
            dialog.setInputMode(QInputDialog.TextInput)
            dialog.setLabelText("Enter bookmark title:")
            dialog.setCancelButtonText("Cancel")
            dialog.resize(300, 150)  # Optional: Resize the dialog if needed

            # Show the dialog and wait for the user input
            if dialog.exec_() == QInputDialog.Accepted:
                bookmark_title = dialog.textValue()
                if bookmark_title:  # If the user entered a title
                    bookmark_btn = QPushButton(bookmark_title)
                    bookmark_btn.setStyleSheet(
                        """
                        QPushButton {
                            background-color: white;
                            color: red;
                            border: 2px solid #0f0;
                            font-family: "Press Start 2P";
                        }
                        QPushButton:hover {
                            background-color: #111;
                        }
                        """
                    )
                    bookmark_btn.clicked.connect(
                        lambda: self.tab_widget.currentWidget().setUrl(QUrl(url))
                    )

                    # Context menu for deleting bookmarks
                    bookmark_btn.setContextMenuPolicy(Qt.CustomContextMenu)
                    bookmark_btn.customContextMenuRequested.connect(
                        lambda pos, btn=bookmark_btn: self.show_bookmark_menu(pos, btn)
                    )

                    # Add the bookmark button to the bookmark bar
                    self.bookmark_bar_layout.addWidget(bookmark_btn)
                    self.bookmarks.append((bookmark_title, url, bookmark_btn))

    def load_background_music(self):
        # Path to the music file
        playlist = QMediaPlaylist()
        music_path = os.path.join(self.script_dir, "bgm", "sdp.mp3")
        url = QUrl.fromLocalFile(music_path)
        content = QMediaContent(url)
        playlist.addMedia(QMediaContent(url))
        playlist.setPlaybackMode(QMediaPlaylist.Loop)

        # Assign the playlist to the media player
        self.music_player.setPlaylist(playlist)
        self.music_player.setMedia(content)
        self.music_player.play()

    def set_volume(self, value):
        self.music_player.setVolume(value)

    def show_bookmark_menu(self, pos, bookmark_btn):
        menu = QMenu(self)
        delete_action = menu.addAction("Delete Bookmark")

        action = menu.exec_(bookmark_btn.mapToGlobal(pos))

        if action == delete_action:
            # Remove the button from the layout
            bookmark_btn.setParent(None)
            bookmark_btn.deleteLater()

            # Remove the bookmark from the list
            self.bookmarks = [b for b in self.bookmarks if b[2] != bookmark_btn]

    def mouse_press_event(self, event):
        self.old_position = event.globalPos()

    def mouse_move_event(self, event):
        delta = QPoint(event.globalPos() - self.old_position)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.old_position = event.globalPos()

    def load_custom_font(self):
        # Load the font from the local file and add it to the QFontDatabase
        font_id = QFontDatabase.addApplicationFont(
            os.path.join(self.script_dir, "fonts", "PressStart2P.ttf")
        )
        if font_id == -1:
            print("Failed to load font")
        else:
            print("Font successfully loaded")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("OR-BIT Browser")
    window = Browser()
    window.show()
    sys.exit(app.exec_())
