
# OR-BIT Browser

OR-BIT Browser is a custom lightweight web browser built with PyQt5 and QWebEngineView. It features a frameless window with a custom title bar, multiple tab support, a bookmark system, and a built-in music player. The browser also supports developer tools for web development.
## DEMO VIDEO:

https://github.com/user-attachments/assets/6b1f9a65-9340-472e-adcd-342165cb44f0

## a glimpse 
![Screenshot 2024-09-30 163414](https://github.com/user-attachments/assets/2ebdcec2-9798-4e7d-8572-4430cc11d3d8)

![Screenshot 2024-09-30 163438](https://github.com/user-attachments/assets/672d385d-4260-45cf-bef1-3cb329b3a628)

![Screenshot 2024-09-30 163503](https://github.com/user-attachments/assets/476dedc8-0155-4957-a429-af91fbadaae8)

![Screenshot 2024-09-30 163720](https://github.com/user-attachments/assets/148224b1-c9be-47fd-89b2-83656a314d29)

![Screenshot 2024-09-30 163857](https://github.com/user-attachments/assets/f494ed18-bf2a-4034-b804-0c3c58a499ff)

## Features

- **Custom Title Bar**: The browser has a custom title bar with minimize, maximize, and close buttons.
- **Frameless Window**: The window has no default title bar or window borders, offering a modern, minimalist look.
- **Tabs**: The browser supports multiple tabs with a '+' button to open new tabs.
- **Bookmarks**: Users can bookmark pages, which will be displayed on a thin bookmark bar. Right-clicking on a bookmark allows you to delete it.
- **Developer Tools**: The browser includes an optional developer tools window that can be toggled on or off.
- **Background Music**: A background music player plays a looping music file. The volume can be adjusted using a slider in the navigation bar.
- **Custom Fonts and Styling**: The browser uses the "Press Start 2P" font, giving it a retro, 8-bit aesthetic.
- **Navigation Bar**: The navigation bar includes buttons for going back, forward, refreshing, and returning to the homepage.

## How to Use

1. **Running the Browser**: 
   To start the browser, simply run the Python script:
   ```bash
   python browser.py
   ```

2. **Basic Navigation**:
   - Use the URL bar to enter a website address and press Enter to navigate.
   - Use the back and forward buttons to navigate through your browser history.
   - Press the home button to return to the default home page (Google).

3. **Tabs**:
   - New tabs can be added using the '+' button on the tab bar.
   - Close a tab by pressing the 'x' button on the tab.

4. **Bookmarks**:
   - Add a bookmark by clicking the heart icon in the navigation bar. You will be prompted to enter a name for the bookmark.
   - Bookmarks will appear in the bookmark bar under the navigation bar.
   - Right-click a bookmark to delete it.

5. **Developer Tools**:
   - The developer tools can be toggled using the inspect button in the navigation bar.

6. **Background Music**:
   - Background music plays automatically upon starting the browser.
   - Adjust the music volume using the volume slider in the navigation bar.

## Project Structure

```bash
OR-BIT/
├── browser.py          # Main Python file for running the OR-BIT browser
├── images/             # Directory for icons used in the navigation bar and title bar
│   ├── back.png
│   ├── heart.png
│   ├── home.png
│   ├── inspect.png
│   ├── logo.png
│   └── undo.png
├── bgm/                # Directory for background music
│   └── sdp.mp3
├── fonts/              # Directory for custom fonts
│   └── PressStart2P.ttf
└── webengine/          # Directory for WebEngine persistent storage
```

## Dependencies

- PyQt5: To install PyQt5, use pip:
  ```bash
  pip install PyQt5 PyQtWebEngine
  ```

## Future Enhancements

- **Dark Mode Toggle**: Add an option to toggle between light and dark modes.
- **Customizable Home Page**: Allow users to set a custom home page.
- **Enhanced Bookmark Management**: Provide more options for organizing and managing bookmarks.
- **Integrated Search Engine**: Add a search bar with a configurable search engine (e.g., Google, DuckDuckGo).

## License

This project is licensed under the MIT License. Feel free to use and modify it for your own purposes.
