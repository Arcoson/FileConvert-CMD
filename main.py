#!/usr/bin/env python3
import argparse
import os
from pathlib import Path
from PIL import Image
import cairosvg
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.prompt import Prompt
from rich.table import Table
from rich.markdown import Markdown

console = Console()

SUPPORTED_FORMATS = {
    'PNG': ['.png'],
    'JPEG': ['.jpg', '.jpeg'], 
    'SVG': ['.svg'],
    'WEBP': ['.webp'],
    'BMP': ['.bmp'],
    'GIF': ['.gif'],
    'TIFF': ['.tiff', '.tif']
}

def show_welcome():
    welcome_text = """
# 🖼️ FileConvert

Welcome to FileConvert! This tool helps you convert images between different formats.

## Commands:
- `convert`: Convert an image from one format to another
- `help`: Show this help message
- `formats`: Show supported formats
- `exit`: Exit the program
    """
    console.print(Markdown(welcome_text))

def show_formats():
    table = Table(title="Supported Image Formats")
    table.add_column("Format", style="cyan")
    table.add_column("Extensions", style="green")
    
    for format_name, extensions in SUPPORTED_FORMATS.items():
        table.add_row(format_name, ", ".join(extensions))
    
    console.print(table)

def get_format_from_extension(ext):
    for format_name, extensions in SUPPORTED_FORMATS.items():
        if ext.lower() in extensions:
            return format_name
    return None

def convert_image(input_path: str, output_path: str) -> bool:
    try:
        input_ext = os.path.splitext(input_path)[1].lower()
        output_ext = os.path.splitext(output_path)[1].lower()

        # Handle SVG conversion separately
        if input_ext == '.svg':
            if output_ext in ['.png', '.jpg', '.jpeg']:
                cairosvg.svg2png(url=input_path, write_to=output_path)
                return True
        elif output_ext == '.svg':
            console.print("[red]Converting to SVG is not supported[/]")
            return False
        
        # Handle other image formats
        with Image.open(input_path) as img:
            # Convert RGBA to RGB if saving as JPEG
            if output_ext in ['.jpg', '.jpeg'] and img.mode == 'RGBA':
                img = img.convert('RGB')
            
            # Save with high quality
            if output_ext in ['.jpg', '.jpeg']:
                img.save(output_path, quality=95, optimize=True)
            else:
                img.save(output_path, optimize=True)
        return True

    except Exception as e:
        console.print(f"[red]Error during conversion: {str(e)}[/]")
        return False

def convert_command():
    input_path = Prompt.ask("Enter input image path")
    if not os.path.exists(input_path):
        console.print("[red]Error: Input file does not exist[/]")
        return

    output_path = Prompt.ask("Enter output image path (with desired extension)")
    
    input_format = get_format_from_extension(os.path.splitext(input_path)[1])
    output_format = get_format_from_extension(os.path.splitext(output_path)[1])

    if not input_format or not output_format:
        console.print("[red]Error: Unsupported file format[/]")
        show_formats()
        return

    console.print(Panel.fit(
        f"[bold green]Image Format Converter[/]\n"
        f"Converting: [cyan]{os.path.basename(input_path)}[/] → [cyan]{os.path.basename(output_path)}[/]",
        border_style="green"
    ))

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console
    ) as progress:
        task = progress.add_task("Converting...", total=100)
        progress.update(task, advance=50)
        
        success = convert_image(input_path, output_path)
        progress.update(task, advance=50)

        if success:
            console.print("[green]Conversion completed successfully! ✨[/]")
        else:
            console.print("[red]Conversion failed! ❌[/]")

def main():
    show_welcome()
    
    while True:
        command = Prompt.ask("\nEnter command", choices=["convert", "help", "formats", "exit"])
        
        if command == "convert":
            convert_command()
        elif command == "help":
            show_welcome()
        elif command == "formats":
            show_formats()
        elif command == "exit":
            console.print("[yellow]Thanks for using FileConvert! Goodbye! 👋[/]")
            break

if __name__ == "__main__":
    main()
