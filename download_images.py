#!/usr/bin/env python3
"""
Image Downloader Script
Downloads all images from a website including:
- <img> tags
- CSS background-image URLs

Usage:
    python download_images.py [url]
    
If no URL is provided, defaults to: https://rayo-nextjs-creative-template.netlify.app/
"""

import os
import re
import sys
import requests
from urllib.parse import urljoin, urlparse, unquote
from bs4 import BeautifulSoup
from pathlib import Path
import time

class ImageDownloader:
    def __init__(self, base_url, output_dir="images"):
        """
        Initialize the ImageDownloader.
        
        Args:
            base_url: The base URL of the website to crawl
            output_dir: Directory to save downloaded images
        """
        self.base_url = base_url.rstrip('/')
        self.output_dir = Path(output_dir)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Track downloaded images
        self.downloaded_images = []
        self.failed_downloads = []
        self.visited_urls = set()
        
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(exist_ok=True)
        
    def is_valid_image_url(self, url):
        """
        Check if URL points to an image file.
        
        Args:
            url: URL to check
            
        Returns:
            bool: True if URL appears to be an image
        """
        if not url:
            return False
            
        # Common image extensions
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', 
                          '.bmp', '.ico', '.tiff', '.tif', '.avif']
        
        # Check if URL ends with image extension
        parsed = urlparse(url.lower())
        path = unquote(parsed.path)
        
        # Check extension
        if any(path.endswith(ext) for ext in image_extensions):
            return True
            
        # Check if URL contains image-related keywords (for data URLs or API endpoints)
        if any(keyword in url.lower() for keyword in ['image', 'img', 'photo', 'picture', 'asset']):
            # But exclude non-image files
            if any(exclude in url.lower() for exclude in ['.js', '.css', '.html', '.json']):
                return False
            return True
            
        return False
    
    def normalize_url(self, url):
        """
        Normalize and resolve relative URLs to absolute URLs.
        
        Args:
            url: URL to normalize
            
        Returns:
            str: Normalized absolute URL or None if invalid
        """
        if not url:
            return None
            
        # Remove data URLs (we'll handle them separately if needed)
        if url.startswith('data:'):
            return None
            
        # Remove fragments and query params for comparison
        url = url.split('#')[0].split('?')[0]
        
        # Handle relative URLs
        if url.startswith('//'):
            url = 'https:' + url
        elif url.startswith('/'):
            url = self.base_url + url
        elif not url.startswith('http'):
            url = urljoin(self.base_url + '/', url)
            
        return url
    
    def extract_images_from_html(self, html_content, page_url):
        """
        Extract image URLs from HTML content.
        
        Args:
            html_content: HTML content as string
            page_url: URL of the page being parsed
            
        Returns:
            set: Set of image URLs found
        """
        images = set()
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find all <img> tags
        for img in soup.find_all('img'):
            src = img.get('src') or img.get('data-src') or img.get('data-lazy-src')
            if src:
                normalized = self.normalize_url(src)
                if normalized and self.is_valid_image_url(normalized):
                    images.add(normalized)
        
        # Find all <source> tags (for responsive images)
        for source in soup.find_all('source'):
            srcset = source.get('srcset')
            if srcset:
                # Parse srcset (format: "url1 width1, url2 width2")
                for item in srcset.split(','):
                    url = item.strip().split()[0] if item.strip() else item.strip()
                    normalized = self.normalize_url(url)
                    if normalized and self.is_valid_image_url(normalized):
                        images.add(normalized)
        
        # Find images in style attributes
        for element in soup.find_all(style=True):
            style = element.get('style', '')
            images.update(self.extract_css_images(style, page_url))
        
        # Find all <link> tags that might reference images
        for link in soup.find_all('link', rel='preload'):
            href = link.get('href')
            as_type = link.get('as', '').lower()
            if as_type == 'image' and href:
                normalized = self.normalize_url(href)
                if normalized and self.is_valid_image_url(normalized):
                    images.add(normalized)
        
        return images
    
    def extract_css_images(self, css_content, base_url):
        """
        Extract image URLs from CSS content (including background-image).
        
        Args:
            css_content: CSS content as string
            base_url: Base URL for resolving relative URLs
            
        Returns:
            set: Set of image URLs found
        """
        images = set()
        
        # Pattern to match url() in CSS
        url_pattern = r'url\s*\(\s*["\']?([^"\'()]+)["\']?\s*\)'
        matches = re.findall(url_pattern, css_content, re.IGNORECASE)
        
        for match in matches:
            url = match.strip()
            if url and not url.startswith('data:'):
                normalized = self.normalize_url(url)
                if normalized and self.is_valid_image_url(normalized):
                    images.add(normalized)
        
        return images
    
    def fetch_page(self, url):
        """
        Fetch a page and return its content.
        
        Args:
            url: URL to fetch
            
        Returns:
            tuple: (content, content_type) or (None, None) on error
        """
        if url in self.visited_urls:
            return None, None
            
        self.visited_urls.add(url)
        
        try:
            response = self.session.get(url, timeout=10, allow_redirects=True)
            response.raise_for_status()
            return response.content, response.headers.get('Content-Type', '')
        except requests.RequestException as e:
            print(f"  ⚠️  Error fetching {url}: {e}")
            return None, None
    
    def crawl_css_files(self, html_content):
        """
        Find and crawl CSS files referenced in HTML.
        
        Args:
            html_content: HTML content as string
            
        Returns:
            set: Set of image URLs found in CSS
        """
        css_images = set()
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find all <link> tags with rel="stylesheet"
        for link in soup.find_all('link', rel='stylesheet'):
            href = link.get('href')
            if href:
                css_url = self.normalize_url(href)
                if css_url:
                    print(f"  📄 Crawling CSS: {css_url}")
                    css_content, content_type = self.fetch_page(css_url)
                    if css_content and 'text/css' in content_type:
                        css_images.update(self.extract_css_images(css_content.decode('utf-8', errors='ignore'), css_url))
        
        # Find <style> tags
        for style in soup.find_all('style'):
            css_content = style.string or ''
            css_images.update(self.extract_css_images(css_content, self.base_url))
        
        return css_images
    
    def get_filename(self, url, content_type=None):
        """
        Extract filename from URL or generate one based on content type.
        
        Args:
            url: Image URL
            content_type: HTTP Content-Type header
            
        Returns:
            str: Filename
        """
        parsed = urlparse(url)
        path = unquote(parsed.path)
        filename = os.path.basename(path)
        
        # If no filename in URL, generate one
        if not filename or '.' not in filename:
            # Try to get extension from content type
            ext = '.jpg'  # default
            if content_type:
                if 'png' in content_type:
                    ext = '.png'
                elif 'gif' in content_type:
                    ext = '.gif'
                elif 'webp' in content_type:
                    ext = '.webp'
                elif 'svg' in content_type:
                    ext = '.svg'
            
            # Generate filename from URL path
            path_parts = [p for p in path.split('/') if p]
            if path_parts:
                filename = path_parts[-1] + ext
            else:
                filename = f"image_{hash(url) % 10000}{ext}"
        
        # Clean filename
        filename = re.sub(r'[<>:"|?*]', '_', filename)
        return filename
    
    def handle_duplicate_filename(self, filepath):
        """
        Handle duplicate filenames by adding a number suffix.
        
        Args:
            filepath: Original filepath
            
        Returns:
            Path: Unique filepath
        """
        if not filepath.exists():
            return filepath
        
        base = filepath.stem
        ext = filepath.suffix
        directory = filepath.parent
        
        counter = 1
        while True:
            new_filename = f"{base}_{counter}{ext}"
            new_filepath = directory / new_filename
            if not new_filepath.exists():
                return new_filepath
            counter += 1
    
    def download_image(self, url):
        """
        Download an image from URL.
        
        Args:
            url: Image URL to download
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            response = self.session.get(url, timeout=15, allow_redirects=True, stream=True)
            response.raise_for_status()
            
            # Check if it's actually an image
            content_type = response.headers.get('Content-Type', '')
            if not content_type.startswith('image/'):
                print(f"  ⚠️  Skipping {url} (not an image: {content_type})")
                return False
            
            # Get filename
            filename = self.get_filename(url, content_type)
            filepath = self.output_dir / filename
            
            # Handle duplicates
            filepath = self.handle_duplicate_filename(filepath)
            
            # Download and save
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            file_size = filepath.stat().st_size
            self.downloaded_images.append({
                'url': url,
                'path': str(filepath),
                'size': file_size
            })
            
            print(f"  ✅ Downloaded: {filepath.name} ({file_size:,} bytes)")
            return True
            
        except requests.RequestException as e:
            print(f"  ❌ Failed to download {url}: {e}")
            self.failed_downloads.append({'url': url, 'error': str(e)})
            return False
        except Exception as e:
            print(f"  ❌ Error saving {url}: {e}")
            self.failed_downloads.append({'url': url, 'error': str(e)})
            return False
    
    def crawl(self):
        """
        Main crawling method that discovers and downloads all images.
        """
        print(f"🚀 Starting image download from: {self.base_url}")
        print(f"📁 Output directory: {self.output_dir.absolute()}\n")
        
        # Fetch main page
        print("📄 Fetching main page...")
        html_content, content_type = self.fetch_page(self.base_url)
        
        if not html_content:
            print("❌ Failed to fetch main page. Exiting.")
            return
        
        # Extract images from HTML
        print("🔍 Extracting images from HTML...")
        html_images = self.extract_images_from_html(html_content, self.base_url)
        print(f"  Found {len(html_images)} images in HTML")
        
        # Extract images from CSS
        print("🎨 Extracting images from CSS...")
        css_images = self.crawl_css_files(html_content)
        print(f"  Found {len(css_images)} images in CSS")
        
        # Combine all images
        all_images = html_images | css_images
        print(f"\n📊 Total unique images found: {len(all_images)}\n")
        
        # Download images
        print("⬇️  Downloading images...\n")
        for i, img_url in enumerate(all_images, 1):
            print(f"[{i}/{len(all_images)}] {img_url}")
            self.download_image(img_url)
            time.sleep(0.1)  # Be polite to the server
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """
        Print download summary.
        """
        print("\n" + "="*70)
        print("📊 DOWNLOAD SUMMARY")
        print("="*70)
        print(f"✅ Successfully downloaded: {len(self.downloaded_images)} images")
        print(f"❌ Failed downloads: {len(self.failed_downloads)}")
        print(f"📁 Output directory: {self.output_dir.absolute()}\n")
        
        if self.downloaded_images:
            print("✅ Downloaded Images:")
            print("-" * 70)
            total_size = 0
            for img in self.downloaded_images:
                print(f"  • {img['path']}")
                print(f"    URL: {img['url']}")
                print(f"    Size: {img['size']:,} bytes")
                total_size += img['size']
                print()
            print(f"📦 Total size: {total_size:,} bytes ({total_size / 1024 / 1024:.2f} MB)")
        
        if self.failed_downloads:
            print("\n❌ Failed Downloads:")
            print("-" * 70)
            for failed in self.failed_downloads:
                print(f"  • {failed['url']}")
                print(f"    Error: {failed['error']}")
                print()


def main():
    """Main entry point."""
    # Default URL
    default_url = "https://rayo-nextjs-creative-template.netlify.app/"
    
    # Get URL from command line or use default
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = default_url
    
    # Validate URL
    if not url.startswith(('http://', 'https://')):
        print("❌ Error: URL must start with http:// or https://")
        print(f"Usage: python {sys.argv[0]} [url]")
        sys.exit(1)
    
    # Create downloader and start crawling
    downloader = ImageDownloader(url)
    downloader.crawl()


if __name__ == "__main__":
    main()
