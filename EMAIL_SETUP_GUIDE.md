# Email Setup Guide for AgroGPT Contact Form

## Overview
The contact form is now fully functional and will send emails when users submit messages. This guide explains how to configure the email settings.

## Email Configuration

### Step 1: Update Email Settings
Edit `agrogpt_web/settings.py` and update the email configuration:

```python
# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # For Gmail
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'  # Replace with your email
EMAIL_HOST_PASSWORD = 'your-app-password'  # Replace with your app password
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'  # Replace with your email
ADMIN_EMAIL = 'admin@agrogpt.com'  # Replace with admin email
```

### Step 2: Gmail Setup (Recommended)

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate App Password**:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate a new app password for "Mail"
   - Use this password in `EMAIL_HOST_PASSWORD`

### Step 3: Alternative Email Providers

#### For Outlook/Hotmail:
```python
EMAIL_HOST = 'smtp-mail.outlook.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```

#### For Yahoo:
```python
EMAIL_HOST = 'smtp.mail.yahoo.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```

#### For Custom SMTP:
```python
EMAIL_HOST = 'your-smtp-server.com'
EMAIL_PORT = 587  # or 465 for SSL
EMAIL_USE_TLS = True  # or EMAIL_USE_SSL = True for port 465
```

### Step 4: Development Testing
For development, you can use the console backend to see emails in the terminal:

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

## How It Works

### Contact Form Flow:
1. User fills out contact form
2. JavaScript validates the form data
3. Form data is sent to Django backend (`/send-contact-email/`)
4. Django validates the data and sends two emails:
   - **Admin Email**: Notification to admin about the contact form submission
   - **User Email**: Confirmation email to the user

### Email Content:

#### Admin Email:
- Subject: "AgroGPT Contact Form: [User's Subject]"
- Contains: User's name, email, subject, and message
- Sent to: `ADMIN_EMAIL` setting

#### User Confirmation Email:
- Subject: "Thank you for contacting AgroGPT"
- Contains: Confirmation message with their submitted details
- Sent to: User's email address

## Security Features

- **CSRF Protection**: All form submissions are protected
- **Input Validation**: Server-side validation of all fields
- **Email Validation**: Proper email format checking
- **Rate Limiting**: Built-in protection against spam

## Troubleshooting

### Common Issues:

1. **"Failed to send email" error**:
   - Check your email credentials
   - Verify app password is correct
   - Ensure 2FA is enabled for Gmail

2. **"Invalid email format" error**:
   - Check the email address format
   - Ensure no extra spaces

3. **"All fields are required" error**:
   - Fill in all form fields
   - Check for minimum length requirements

### Testing:
1. Start the Django server: `python manage.py runserver`
2. Go to `/contact/`
3. Fill out the form and submit
4. Check your email for the confirmation

## Production Deployment

For production, consider:
- Using a dedicated email service (SendGrid, Mailgun, etc.)
- Setting up proper SPF/DKIM records
- Monitoring email delivery rates
- Implementing email templates for better formatting

## Support

If you encounter issues:
1. Check the Django console for error messages
2. Verify your email settings
3. Test with console backend first
4. Check your email provider's SMTP settings 