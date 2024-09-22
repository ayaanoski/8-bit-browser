![Screenshot 2024-09-22 034621](https://github.com/user-attachments/assets/260cef0e-7636-4567-8131-6930b32281f4)# 8-Bit Retro Browser

Welcome to the 8-Bit Retro Browser! This application is a fun and nostalgic web browser that incorporates a retro 8-bit aesthetic. Built using PyQt5, it allows users to navigate the web while enjoying a unique visual style reminiscent of classic video games.


![Screenshot 2024-09-22 034621](https://github.com/user-attachments/assets/79f1f4eb-cfe8-4d7e-9e59-25ba7f2a5953)

![Screenshot 2024-09-22 034809](https://github.com/user-attachments/assets/ee0a8387-66ca-460b-9c41-2dee1e73de1f)

![Screenshot 2024-09-22 034653](https://github.com/user-attachments/assets/1df37bb0-ccef-4fbf-bb39-0b32af731dce)

![Screenshot 2024-09-22 034726](https://github.com/user-attachments/assets/3075e888-b40e-49b1-b64b-ea7a78c4671f)


## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Customization](#customization)
- [License](#license)
- [Contributing](#contributing)

## Features

- **Retro Aesthetic**: Enjoy a nostalgic 8-bit style with custom fonts and colors.
- **Navigation Bar**: Easily navigate with back, forward, refresh, and home buttons.
- **URL Entry**: Enter URLs directly or search via Google.
- **Custom Logo**: The Google homepage features a pixelated logo for added retro flair.
- **Dark Mode**: Enhanced visibility with a dark background and bright text.

## Installation

To run the 8-Bit Retro Browser, you'll need to have Python and PyQt5 installed on your machine. Follow these steps:

1. **Install Python**: Ensure you have Python 3.x installed. You can download it from [python.org](https://www.python.org/).
2. **Install PyQt5**: Use pip to install the required packages:
    ```bash
    pip install PyQt5 PyQtWebEngine
    ```
3. **Download the Source Code**: Clone or download this repository to your local machine.
4. **Add Icons**: Ensure you have the necessary icon images (logo, back, forward, refresh, home) in the specified paths or update the paths in the code accordingly.

## Usage

1. **Run the Application**:
    ```bash
    python browser.py
    ```
   Replace `browser.py` with the name of your Python file if different.

2. **Navigate the Web**:
   - Use the URL bar to enter any web address or search term.
   - Click on navigation buttons to go back, forward, refresh the page, or return to Google.

3. **Experience the 8-Bit Style**:
   - The browser automatically applies an 8-bit style to all loaded pages.
   - The Google homepage will display a custom pixelated logo.

## Customization

You can customize various aspects of the browser:

- **Icons**: Update the paths for icons in the code to use your own images.
- **Styling**: Modify the CSS within the `apply_8bit_style` method to change colors or styles as desired.
- **Fonts**: Change the font by updating the `font-family` property in the stylesheet.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! If you have suggestions or improvements, feel free to fork this repository and submit a pull request. Enjoy browsing with a touch of nostalgia! If you encounter any issues or have questions, please feel free to reach out. Happy surfing!
