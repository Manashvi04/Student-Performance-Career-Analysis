import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading

def send_email_async(app_name, sender_email, sender_password, smtp_server, smtp_port, recipient, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = f"{app_name} <{sender_email}>"
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))
        
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print(f"Successfully sent credentials to {recipient}")
    except Exception as e:
        print(f"Failed to send email to {recipient}: {e}")

def send_credentials_email(email, role, password):
    sender_email = os.environ.get("SMTP_USERNAME")
    sender_password = os.environ.get("SMTP_PASSWORD")
    smtp_server = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
    
    try:
        smtp_port = int(os.environ.get("SMTP_PORT", 587))
    except ValueError:
        smtp_port = 587
        
    app_name = "Student Performance Analyzer"
    
    if not sender_email or not sender_password:
        print("SMTP_USERNAME or SMTP_PASSWORD not found in environment variables. Skipping email.")
        return
        
    subject = f"Your {role.capitalize()} Account Credentials"
    body = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #eee; border-radius: 8px;">
                <h2 style="color: #4CAF50;">Welcome to {app_name}!</h2>
                <p>An account has been created for you with the role: <strong>{role.capitalize()}</strong>.</p>
                <div style="background-color: #f9f9f9; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <p style="margin: 0;">Your automatically generated password is:</p>
                    <h3 style="margin: 10px 0; color: #d32f2f; letter-spacing: 2px;">{password}</h3>
                </div>
                <p>Please log in using this password. We recommend changing it after your first login.</p>
                <hr style="border: none; border-top: 1px solid #ccc; margin: 20px 0;" />
                <p style="font-size: 0.9em; color: #777;">If you did not request this account, please contact the administrator.</p>
            </div>
        </body>
    </html>
    """
    
    # Run in background to avoid blocking the main server thread
    thread = threading.Thread(target=send_email_async, args=(
        app_name, sender_email, sender_password, smtp_server, smtp_port, email, subject, body
    ))
    # setting daemon to True so the thread doesn't prevent app from exiting
    thread.daemon = True
    thread.start()
