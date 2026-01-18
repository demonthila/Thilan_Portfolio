# Contact Form Setup Instructions

## Problem
PHP `mail()` function doesn't work on static hosting services like GitHub Pages. Your contact form needs a backend server or a third-party service to send emails.

## Solution Options

### Option 1: EmailJS (Recommended for Static Sites)
EmailJS works on static sites without a backend. Free plan: 200 emails/month.

#### Setup Steps:
1. **Sign up for EmailJS**: Go to https://www.emailjs.com/ and create a free account
2. **Connect Gmail**:
   - In EmailJS dashboard, go to "Email Services"
   - Click "Add New Service"
   - Choose "Gmail" and connect your Gmail account (sanjulathilan12321@gmail.com)
3. **Create Email Template**:
   - Go to "Email Templates"
   - Click "Create New Template"
   - Use this template:
     ```
     Subject: Contact Form Message from {{Name}}
     
     You have received a new message from your portfolio contact form.
     
     Name: {{Name}}
     Email: {{E-mail}}
     Message: {{Message}}
     ```
   - Save and note your Template ID
4. **Get your Service ID and Public Key**:
   - Service ID: Found in "Email Services" (e.g., `service_xxxxx`)
   - Public Key: Found in "Account" > "General" (e.g., `xxxxx`)
   - Template ID: From the template you created (e.g., `template_xxxxx`)

5. **Update the form code** with your EmailJS credentials (see below)

### Option 2: Formspree (Alternative)
1. Sign up at https://formspree.io/
2. Create a new form
3. Update form action to: `action="https://formspree.io/f/YOUR_FORM_ID"`

### Option 3: Use a Server with PHP
If you have a server with PHP support, ensure:
- PHP mail() is configured
- Check server logs for errors
- Verify email isn't going to spam folder

## Testing the Form
1. Open browser console (F12)
2. Submit the form
3. Check for any errors in console
4. Check spam folder for test emails
