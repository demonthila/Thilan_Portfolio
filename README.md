# Sanjula Thilan portfolio

## Pages
- index.html: Home (hero, selected work, playground teaser, about teaser, quote, contact)
- work/dela.html, work/active-care.html, work/iom-world.html, work/novalink.html: case studies
- about.html: journey, principles, testimonials, education
- play.html: OrangeHRM, brand identities, workforce graphics, AI marketing videos, visual studies
- contact.html: three ways in (brief form, book a call, email); the form posts to mail.php
- 404.html: page-not-found

## Editing
All text lives in build.py. Change it, then run `python3 build.py` to rebuild every page.
Styles are in assets/css/site.css and behaviour in assets/js/site.js.
Images are in assets/img, videos in assets/video.

## Upload
Upload everything except build.py, README.md and the dot-folders to your hosting root, keeping the folder structure.
.htaccess redirects the old /HTML/... addresses to the new pages, so existing links keep working.

## Before going live
1. Resume: upload a PDF and change RESUME in build.py to its path.
2. Impact: search build.py for "Replace with a measured result" and add real numbers when you have them.
3. Process images: add wireframes, flows and journey maps as extra slides in each case study gallery.
