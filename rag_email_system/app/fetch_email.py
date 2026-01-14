import imaplib
import email
from email.header import decode_header
from load_environment import LoadEnvironment


class FetchEmail:

    # Method to Fetch Emails from Email Server
    @staticmethod
    def fetch_email(username, password,limit=100):

        # Connection to Email Server
        mail = imaplib.IMAP4_SSL(LoadEnvironment.IMAP_SERVER)
        # Login into Email using Username and App Password
        mail.login(username, password)
        # Select Messages from Inbox
        mail.select("inbox")

        # Search ALL Emails in Email Inbox and Get Only Last 100 Emails
        _, data = mail.search(None, "ALL")
        email_ids = data[0].split()[-limit:]

        emails = []

        # Loop Through Each Email
        for eid in email_ids:
            # Fetch Full Email Content and Convert Raw Bytes to Email Object
            _, msg_data = mail.fetch(eid, "(RFC822)")
            msg = email.message_from_bytes(msg_data[0][1])

            # Extract Subject from Email
            subject, _ = decode_header(msg["Subject"])[0]
            subject = subject.decode() if isinstance(subject, bytes) else subject

            # Extract Only Readable Parts in Email
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body += part.get_payload(decode=True).decode(errors="ignore")
            else:
                body = msg.get_payload(decode=True).decode(errors="ignore")

            # Store Extracted Data
            emails.append({
                "subject": subject,
                "body": body
            })

        return emails
