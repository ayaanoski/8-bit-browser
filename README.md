# OR-BIT Browser

## Overview
OR-BIT is a lightweight, 8-bit themed web browser built with PyQt5 and QtWebEngine. The browser features a custom user interface with a unique title bar, navigation buttons, and the ability to manage multiple tabs. It is designed to provide a fun and nostalgic browsing experience while offering essential features like bookmarks and volume control.

## Features
- **Custom Title Bar**: A sleek title bar with custom buttons for minimizing, maximizing, and closing the window.
- **Multiple Tabs**: Users can open multiple tabs, with the option to close them as needed.
- **Navigation Controls**: Back, forward, refresh, and home buttons for easy navigation.
- **URL Bar**: An input field to enter URLs and navigate directly to websites.
- **Bookmarks**: Users can add bookmarks with custom titles and manage them through a context menu.
- **Volume Control**: A slider to control the background music volume.
- **Developer Tools**: Access to developer tools via a dockable widget for debugging web pages.
- **8-bit Theming**: Custom CSS applied to web pages for a unique 8-bit style.
- **Background Music**: A looped background music feature to enhance the browsing experience.

## Installation
To run the OR-BIT Browser, ensure you have Python installed along with the necessary packages. You can install the required dependencies using pip:

```bash
pip install PyQt5 PyQtWebEngine
```

## Usage
1. **Run the Application**: Execute the `main.py` script to launch the browser.
   ```bash
   python main.py
   ```
2. **Navigating**: Use the URL bar to enter web addresses or click on the navigation buttons.
3. **Managing Tabs**: Click on the "+" button to open a new tab. Close tabs by clicking the "X" on the tab.
4. **Adding Bookmarks**: While on a desired page, click the bookmark button to save the page with a custom title.
5. **Accessing Developer Tools**: Use the inspect button to toggle the developer tools dock.

## Customization
- To customize the look of the browser, you can modify the CSS and UI elements within the code.
- You can change the background music by replacing the `sdp.mp3` file in the `bgm` directory.

## License
This project is open-source and available for anyone to use and modify. Feel free to contribute!

## Acknowledgments
- The 8-bit style is inspired by retro gaming aesthetics.
- Special thanks to the PyQt5 and QtWebEngine documentation for guidance on building this application.

