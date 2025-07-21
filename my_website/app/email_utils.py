import os

import resend
from dotenv import load_dotenv

load_dotenv()  # THIS MUST BE CALLED EARLY
resend.api_key = os.getenv("EMAIL_KEY_RESEND")


def send_email(email_to: str, user_id):
    attachment: resend.Attachment = {
      "path": f"https://kathamritam.online/static/qr_codes/{user_id}.png",
      "filename": f"qr_{user_id}.png",
    }
    # attachment: resend.Attachment = {
    #     "path": "https://resend.com/static/sample/invoice.pdf",
    #     "filename": "invoice.pdf",
    # }

    params: resend.Emails.SendParams = {
        "from": "Bhagavata Kathamritam Info <info@kathamritam.online>",
        "to": [email_to],
        "subject": "QR Code for offline pass",
        "attachments": [attachment],
        "html": """
        <!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body {
      font-family: Arial, sans-serif;
      line-height: 1.6;
      color: #333;
      margin: 0;
      padding: 0;
    }
    .container {
      max-width: 600px;
      margin: 0 auto;
      padding: 20px;
      background-color: #f9f9f9;
    }
    .header {
      background-color: #d4a017;
      color: #fff;
      padding: 10px;
      text-align: center;
      border-radius: 5px 5px 0 0;
    }
    .content {
      background-color: #fff;
      padding: 20px;
      border-radius: 0 0 5px 5px;
      box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .footer {
      text-align: center;
      font-size: 12px;
      color: #777;
      margin-top: 20px;
    }
    .button {
      display: inline-block;
      padding: 10px 20px;
      margin: 10px 0;
      background-color: #d4a017;
      color: #fff;
      text-decoration: none;
      border-radius: 5px;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h2>Bhagavata Kathamrita - Your QR Code & Verification</h2>
    </div>
    <div class="content">
      <p>Dear Devotee,</p>
      <p>We are delighted to confirm that your registration for the <strong>Bhagavata Kathamrita</strong> event has been successfully verified! Attached to this email, you will find your unique QR code, which will allow you to collect your offline pass at the event stall.</p>
      <p><strong>How to Get Your Offline Pass:</strong></p>
      <ul>
        <li>Save the attached QR code to your mobile device or print it for convenience.</li>
        <li>Visit the Bhagavata Kathamrita event stall on the day of the event.</li>
        <li>Present the QR code to our team to receive your offline pass.</li>
      </ul>
      <p>We are thrilled to have you join us for this divine experience of spiritual wisdom and devotion. If you have any questions or require further assistance, please feel free to contact us.</p>
      <p>Wishing you a blessed and enriching experience at Bhagavata Kathamrita!</p>
      <p>With warm regards,<br>The Bhagavata Kathamrita Team</p>
    </div>
    <div class="footer">
      <p>© 2025 Bhagavata Kathamrita Organizers. All rights reserved.</p>
    </div>
  </div>
</body>
</html>"""
    }

    try:
      email = resend.Emails.send(params)
      return {'success': True, 'email': email}
    except Exception as e:
      return {'success': False, 'error': str(e)}
