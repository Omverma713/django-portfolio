from django.shortcuts import render, redirect
from django.contrib import messages
import resend
from django.conf import settings
import requests


def home(request):

    if request.method == "POST":
        resend.api_key = settings.RESEND_API_KEY
        # ===========================
        # Cloudflare Turnstile Check
        # ===========================

        token = request.POST.get("cf-turnstile-response")

        if not token:
            messages.error(
                request,
                "Please complete the security verification."
            )
            return redirect("/#contact")

        verify = requests.post(
            "https://challenges.cloudflare.com/turnstile/v0/siteverify",
            data={
                "secret": settings.TURNSTILE_SECRET_KEY,
                "response": token,
            },
            timeout=10,
        )

        result = verify.json()

        if not result.get("success"):
            messages.error(
                request,
                "Verification failed. Please try again."
            )
            return redirect("/#contact")

        # ===========================
        # Contact Form Data
        # ===========================

        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        subject = request.POST.get("subject", "").strip()
        message = request.POST.get("message", "").strip()

        subject_line = f"📩 New Portfolio Message • {subject}"

        # ====================================
        # PREMIUM EMAIL (To You)
        # Part 2 continues from here...
        # ====================================

        html_message = f""" <html>

<head>

<meta charset="UTF-8">

</head>

<body style="margin:0;padding:0;background:#eef2ff;font-family:Arial,Helvetica,sans-serif;">

<table width="100%" cellpadding="0" cellspacing="0" style="background:#eef2ff;padding:40px 0;">

<tr>

<td align="center">

<table width="680" cellpadding="0" cellspacing="0"
style="background:#ffffff;border-radius:22px;overflow:hidden;
box-shadow:0 15px 40px rgba(0,0,0,.12);">

<!-- Header -->

<tr>

<td
style="background:linear-gradient(135deg,#6d28d9,#7c3aed,#8b5cf6);
padding:45px;
text-align:center;">

<h1 style="margin:0;color:white;font-size:34px;">

🚀 Portfolio Contact

</h1>

<p style="margin-top:14px;color:#ede9fe;font-size:17px;">

Someone has contacted you through your portfolio.

</p>

</td>

</tr>

<!-- Body -->

<tr>

<td style="padding:45px;">

<h2 style="margin-top:0;color:#7c3aed;">

New Contact Form Submission

</h2>

<p style="font-size:16px;color:#555;line-height:28px;">

A visitor has submitted your portfolio contact form.

</p>

<table
width="100%"
cellpadding="16"
style="margin-top:30px;border-collapse:collapse;background:#fafafa;
border-radius:16px;">

<tr>

<td width="170"
style="font-weight:bold;color:#7c3aed;">

👤 Name

</td>

<td>

{name}

</td>

</tr>

<tr>

<td
style="font-weight:bold;color:#7c3aed;">

📧 Email

</td>

<td>

{email}

</td>

</tr>

<tr>

<td
style="font-weight:bold;color:#7c3aed;">

📝 Subject

</td>

<td>

{subject}

</td>

</tr>

</table>

<div
style="margin-top:35px;
background:#f8f5ff;
padding:28px;
border-left:6px solid #7c3aed;
border-radius:14px;">

<h3
style="margin-top:0;color:#7c3aed;">

💬 Message

</h3>

<p
style="white-space:pre-wrap;
line-height:30px;
color:#444;
font-size:16px;">

{message}

</p>

</div>

<hr
style="margin:45px 0;border:none;border-top:1px solid #ececec;">

<table width="100%">

<tr>

<td>

<h3
style="margin:0;color:#7c3aed;">

⚡ Tech Stack

</h3>

<p
style="margin-top:12px;
color:#666;
line-height:28px;">

Python • Django • React • JavaScript • Tailwind CSS

</p>

</td>

</tr>

</table>

<div
style="margin-top:45px;
text-align:center;">

<a
href="https://github.com/YOUR_USERNAME"
style="display:inline-block;
padding:14px 30px;
background:#111827;
color:white;
text-decoration:none;
border-radius:10px;
margin-right:10px;">

GitHub

</a>

<a
href="https://linkedin.com/in/YOUR_USERNAME"
style="display:inline-block;
padding:14px 30px;
background:#0A66C2;
color:white;
text-decoration:none;
border-radius:10px;">

LinkedIn

</a>

</div>

</td>

</tr>

<tr>

<td
style="background:#fafafa;
padding:25px;
text-align:center;
font-size:13px;
color:#777;">

Built with ❤️ by <strong>Om Verma</strong>

</td>

</tr>

</table>

</td>

</tr>

</table>

</body>

</html>
"""
                # ====================================
        # Send Email To You
        # ====================================

        try:
            resend.Emails.send({
                "from": "Portfolio <onboarding@resend.dev>",
                "to": settings.EMAIL_HOST_USER,
                "subject": subject_line,
                "html": html_message,
            })
        except Exception as e:
            print(e)
            raise

        # ====================================
        # Premium Auto Reply
        # ====================================

        reply_subject = "Thank You For Contacting Me 🚀"

        reply_html = f"""
<html>

<head>

<meta charset="UTF-8">

</head>

<body style="margin:0;padding:0;background:#eef2ff;font-family:Arial,Helvetica,sans-serif;">

<table width="100%" cellpadding="0" cellspacing="0"
style="background:#eef2ff;padding:40px 0;">

<tr>

<td align="center">

<table width="680" cellpadding="0" cellspacing="0"
style="background:#ffffff;border-radius:22px;overflow:hidden;
box-shadow:0 15px 40px rgba(0,0,0,.12);">

<!-- Hero -->

<tr>

<td
style="padding:55px;
text-align:center;
background:linear-gradient(135deg,#6d28d9,#7c3aed,#8b5cf6);">

<h1
style="margin:0;
color:white;
font-size:36px;">

👋 Thank You!

</h1>

<p
style="margin-top:16px;
font-size:18px;
color:#ede9fe;">

Hi {name},

Thank you for contacting me.

</p>

</td>

</tr>

<!-- Body -->

<tr>

<td style="padding:45px;">

<h2 style="color:#7c3aed;margin-top:0;">

Your message has been received successfully.

</h2>

<p
style="font-size:16px;
line-height:30px;
color:#555;">

I really appreciate you taking the time to contact me.

I'll carefully review your message and get back to you as soon as possible.

Usually within 24-48 hours.

</p>

<div
style="margin-top:35px;
background:#f8f5ff;
padding:25px;
border-left:6px solid #7c3aed;
border-radius:14px;">

<h3 style="margin-top:0;color:#7c3aed;">

📨 Your Message

</h3>

<p style="line-height:30px;color:#444;">

<strong>Subject:</strong>

{subject}

</p>

<p
style="white-space:pre-wrap;
line-height:28px;
color:#555;">

{message}

</p>

</div>

<div
style="margin-top:40px;
text-align:center;">
        <a href="https://YOUR-PORTFOLIO.com"
style="
display:inline-block;
padding:14px 28px;
background:#7c3aed;
color:#ffffff;
text-decoration:none;
border-radius:10px;
font-weight:bold;
margin:8px;
">
🌐 Portfolio
</a>

<a href="https://github.com/YOUR_USERNAME"
style="
display:inline-block;
padding:14px 28px;
background:#111827;
color:#ffffff;
text-decoration:none;
border-radius:10px;
font-weight:bold;
margin:8px;
">
💻 GitHub
</a>

<a href="https://linkedin.com/in/YOUR_USERNAME"
style="
display:inline-block;
padding:14px 28px;
background:#0A66C2;
color:#ffffff;
text-decoration:none;
border-radius:10px;
font-weight:bold;
margin:8px;
">
💼 LinkedIn
</a>

<a href="https://YOUR-PORTFOLIO.com/resume.pdf"
style="
display:inline-block;
padding:14px 28px;
background:#16a34a;
color:#ffffff;
text-decoration:none;
border-radius:10px;
font-weight:bold;
margin:8px;
">
📄 Resume
</a>

</div>

<hr style="margin:45px 0;border:none;border-top:1px solid #ececec;">

<p style="
font-size:15px;
color:#666;
line-height:28px;
">

If you have any additional information to share, simply reply to this email.

</p>

<p style="
margin-top:30px;
font-size:15px;
color:#666;
">

Regards,

</p>

<h2 style="
margin-top:8px;
margin-bottom:0;
color:#7c3aed;
">

Om Verma

</h2>

<p style="
margin-top:6px;
color:#777;
">

Full Stack Developer

</p>

</td>

</tr>

<tr>

<td style="
background:#111827;
padding:28px;
text-align:center;
color:#ffffff;
">

<p style="margin:0;font-size:15px;">

© 2026 Om Verma • All Rights Reserved

</p>

<p style="
margin-top:12px;
color:#9ca3af;
font-size:13px;
">

Built with Django • React • Tailwind CSS

</p>

</td>

</tr>

</table>

</td>

</tr>

</table>

</body>

</html>
"""

        try:
            resend.Emails.send({
                "from": "Om Verma <onboarding@resend.dev>",
                "to":email,
                "subject": reply_subject,
                "html": reply_html,
            })
        except Exception as e:
            print(e)
            raise

        messages.success(
            request,
            "✅ Your message has been sent successfully. I'll get back to you soon!"
        )

        return redirect("/#contact")

    return render(
        request,
        "main/index.html",
        {
            "TURNSTILE_SITE_KEY": settings.TURNSTILE_SITE_KEY,
        },
    )