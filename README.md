# FileConvert 🖼️

FileConvert is a command-line image conversion utility written in Python that allows users to convert images between various popular formats. 

## Key Features
- Supports multiple image formats including:
  - PNG
  - JPEG
  - SVG (conversion from SVG to PNG/JPEG)
  - WEBP
  - BMP
  - GIF
  - TIFF

- User-friendly interface with:
  - Interactive command prompt
  - Progress bar for conversions
  - Colorful terminal output using Rich library
  - Clear error messages and feedback

## Commands
- `convert`: Starts the image conversion process
- `formats`: Displays a table of all supported formats
- `help`: Shows the welcome message and available commands
- `exit`: Exits the application

## Technical Details
- Uses PIL (Python Imaging Library) for most image conversions
- Implements CairoSVG for SVG conversions
- Optimizes output images automatically
- Handles RGBA to RGB conversion for JPEG outputs
- Maintains high quality (95%) for JPEG conversions

The application is designed to be both user-friendly for beginners and efficient for batch image conversion needs. It provides clear visual feedback throughout the conversion process and handles errors gracefully.
