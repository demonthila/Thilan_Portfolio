# Image Downloader Script

A Python script to download all images from a website, including images from `<img>` tags and CSS `background-image` URLs.

## Features

- ✅ Crawls HTML pages for `<img>` tags
- ✅ Extracts images from CSS files (background-image, etc.)
- ✅ Handles relative and absolute URLs
- ✅ Automatically handles HTTPS and redirects
- ✅ Preserves original filenames when possible
- ✅ Handles duplicate filenames by adding number suffixes
- ✅ Provides detailed download summary
- ✅ Respects server resources with polite delays

## Requirements

- Python 3.6 or higher
- Required Python packages (see installation below)

## Installation

1. **Install Python dependencies:**

```bash
pip install -r requirements_image_downloader.txt
```

Or install manually:

```bash
pip install requests beautifulsoup4 lxml
```

## Usage

### Basic Usage (Default URL)

Run the script without arguments to download images from the default website:

```bash
python download_images.py
```

### Custom URL

Specify a custom URL as the first argument:

```bash
python download_images.py https://example.com
```

### Examples

```bash
# Download from default URL (rayo template)
python download_images.py

# Download from a custom website
python download_images.py https://example.com

# Download from a local development server
python download_images.py http://localhost:3000
```

## Output

The script will:

1. Create an `images/` directory in your project folder (if it doesn't exist)
2. Download all found images to this directory
3. Print progress as it downloads
4. Display a summary at the end showing:
   - Number of successfully downloaded images
   - Number of failed downloads
   - File paths and sizes
   - Total download size

## How It Works

1. **HTML Parsing**: The script fetches the main page and parses it with BeautifulSoup to find:
   - `<img>` tags (including `src`, `data-src`, `data-lazy-src` attributes)
   - `<source>` tags with `srcset` attributes
   - Images in inline `style` attributes

2. **CSS Parsing**: The script also:
   - Finds and downloads all CSS files referenced in `<link>` tags
   - Parses CSS content to extract `url()` values (background-image, etc.)
   - Extracts images from inline `<style>` tags

3. **Image Download**: For each unique image URL found:
   - Normalizes the URL (handles relative/absolute paths)
   - Downloads the image with proper headers
   - Saves with original filename (or generates one if needed)
   - Handles duplicates by adding number suffixes

## File Structure

After running, your project will have:

```
your-project/
├── download_images.py
├── requirements_image_downloader.txt
└── images/
    ├── image1.jpg
    ├── image2.png
    ├── logo.svg
    └── ...
```

## Troubleshooting

### Import Errors

If you get import errors, make sure all dependencies are installed:

```bash
pip install --upgrade requests beautifulsoup4 lxml
```

### Permission Errors

If you get permission errors when creating the `images/` directory, make sure you have write permissions in the project directory.

### SSL Certificate Errors

If you encounter SSL certificate errors, you can modify the script to disable SSL verification (not recommended for production):

```python
response = self.session.get(url, timeout=10, verify=False)
```

### Timeout Errors

If downloads timeout, you can increase the timeout value in the script:

```python
response = self.session.get(url, timeout=30, ...)
```

## Notes

- The script respects robots.txt and server resources by adding small delays between requests
- Images are validated by checking Content-Type headers
- The script handles common image formats: JPG, PNG, GIF, WebP, SVG, BMP, ICO, TIFF, AVIF
- Duplicate filenames are automatically handled (e.g., `image.jpg`, `image_1.jpg`, `image_2.jpg`)

## License

This script is provided as-is for educational and personal use.
