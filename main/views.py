from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
import requests
import threading


def _send_emails_background(name, email, subject, message, subject_line, html_message, reply_subject, reply_html):
    """
    Sends emails asynchronously in background via Brevo HTTP REST API (Port 443).
    Works 100% on Render Free Tier and delivers both:
    1. Notification to Portfolio Owner with visitor's reply-to.
    2. Automated "Thank You" confirmation email to visitor from Om Verma <omverma.dev@gmail.com>.
    """
    brevo_key = getattr(settings, "BREVO_API_KEY", "")
    owner_email = getattr(settings, "EMAIL_HOST_USER", "omverma.dev@gmail.com")

    headers = {
        "accept": "application/json",
        "api-key": brevo_key,
        "content-type": "application/json"
    }

    # 1. Send Notification to Portfolio Owner
    try:
        data_to_owner = {
            "sender": {"name": "Portfolio Contact", "email": owner_email},
            "to": [{"email": owner_email, "name": "Om Verma"}],
            "replyTo": {"email": email, "name": name or "Visitor"},
            "subject": subject_line,
            "htmlContent": html_message
        }
        res1 = requests.post("https://api.brevo.com/v3/smtp/email", headers=headers, json=data_to_owner, timeout=10)
        print(f"[BREVO ASYNC] Owner notification: {res1.status_code}")
    except Exception as e:
        print(f"[BREVO ASYNC ERROR] Failed sending to owner: {e}")

    # 2. Send Auto-Reply Confirmation to Visitor
    try:
        data_to_visitor = {
            "sender": {"name": "Om Verma", "email": owner_email},
            "to": [{"email": email, "name": name or "Visitor"}],
            "replyTo": {"email": owner_email, "name": "Om Verma"},
            "subject": reply_subject,
            "htmlContent": reply_html
        }
        res2 = requests.post("https://api.brevo.com/v3/smtp/email", headers=headers, json=data_to_visitor, timeout=10)
        print(f"[BREVO ASYNC] Visitor auto-reply: {res2.status_code}")
    except Exception as e:
        print(f"[BREVO ASYNC ERROR] Failed sending to visitor: {e}")



def home(request):

    if request.method == "POST":
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
        # ===================================        # ==========================================================
        # 3D EMAIL TEMPLATE 1: TO PORTFOLIO OWNER (YOU)
        # ==========================================================
        portfolio_url = request.build_absolute_uri('/')
        resume_url = request.build_absolute_uri('/resume/')

        html_message = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>New Portfolio Message</title>
</head>
<body style="margin:0;padding:0;background-color:#070B14;font-family:'Segoe UI',Roboto,Helvetica,Arial,sans-serif;-webkit-font-smoothing:antialiased;">
<table width="100%" cellpadding="0" cellspacing="0" style="background-color:#070B14;padding:40px 15px;">
  <tr>
    <td align="center">
      <!-- Outer 3D Card Shell -->
      <table width="100%" max-width="640" cellpadding="0" cellspacing="0" style="max-width:640px;background:#0d1326;border-radius:28px;border:1px solid rgba(139,92,246,0.3);box-shadow:0 30px 70px rgba(0,0,0,0.8), 0 0 40px rgba(124,58,237,0.25);overflow:hidden;">
        
        <!-- 3D Glow Header -->
        <tr>
          <td style="padding:45px 35px 35px 35px;background:linear-gradient(135deg,#581c87,#7c3aed,#2563eb);text-align:center;position:relative;border-bottom:1px solid rgba(255,255,255,0.15);">
            <div style="display:inline-block;padding:8px 18px;border-radius:50px;background:rgba(0,0,0,0.3);border:1px solid rgba(255,255,255,0.25);margin-bottom:16px;">
              <span style="color:#4ade80;font-size:12px;font-weight:800;letter-spacing:2px;text-transform:uppercase;">⚡ NEW PORTFOLIO LEAD</span>
            </div>
            <h1 style="margin:0;color:#ffffff;font-size:32px;font-weight:900;letter-spacing:-0.5px;text-shadow:0 4px 15px rgba(0,0,0,0.5);">
              Incoming Message
            </h1>
            <p style="margin:10px 0 0 0;color:#e9d5ff;font-size:15px;font-weight:500;">
              Someone just submitted your portfolio contact form
            </p>
          </td>
        </tr>

        <!-- Card Content Body -->
        <tr>
          <td style="padding:35px 30px;">
            
            <!-- Sender Details Inset 3D Grid -->
            <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:25px;">
              <tr>
                <td style="padding:16px 20px;background:#131b35;border-radius:16px;border:1px solid rgba(255,255,255,0.08);box-shadow:inset 0 2px 4px rgba(0,0,0,0.4);margin-bottom:12px;">
                  <table width="100%" cellpadding="0" cellspacing="0">
                    <tr>
                      <td width="32" style="font-size:20px;vertical-align:middle;">👤</td>
                      <td style="padding-left:10px;">
                        <div style="font-size:11px;color:#a78bfa;text-transform:uppercase;font-weight:700;letter-spacing:1px;">Sender Name</div>
                        <div style="font-size:17px;color:#ffffff;font-weight:700;margin-top:2px;">{name}</div>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>
              <tr><td height="12"></td></tr>
              <tr>
                <td style="padding:16px 20px;background:#131b35;border-radius:16px;border:1px solid rgba(255,255,255,0.08);box-shadow:inset 0 2px 4px rgba(0,0,0,0.4);">
                  <table width="100%" cellpadding="0" cellspacing="0">
                    <tr>
                      <td width="32" style="font-size:20px;vertical-align:middle;">📧</td>
                      <td style="padding-left:10px;">
                        <div style="font-size:11px;color:#a78bfa;text-transform:uppercase;font-weight:700;letter-spacing:1px;">Sender Email</div>
                        <div style="font-size:16px;color:#38bdf8;font-weight:600;margin-top:2px;">
                          <a href="mailto:{email}" style="color:#38bdf8;text-decoration:none;">{email}</a>
                        </div>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>
              <tr><td height="12"></td></tr>
              <tr>
                <td style="padding:16px 20px;background:#131b35;border-radius:16px;border:1px solid rgba(255,255,255,0.08);box-shadow:inset 0 2px 4px rgba(0,0,0,0.4);">
                  <table width="100%" cellpadding="0" cellspacing="0">
                    <tr>
                      <td width="32" style="font-size:20px;vertical-align:middle;">📝</td>
                      <td style="padding-left:10px;">
                        <div style="font-size:11px;color:#a78bfa;text-transform:uppercase;font-weight:700;letter-spacing:1px;">Subject</div>
                        <div style="font-size:16px;color:#ffffff;font-weight:700;margin-top:2px;">{subject}</div>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>
            </table>

            <!-- 3D Message Box -->
            <div style="padding:22px;background:#111827;border-radius:18px;border-left:5px solid #8b5cf6;border:1px solid rgba(139,92,246,0.25);border-left-width:5px;box-shadow:inset 0 3px 6px rgba(0,0,0,0.5);margin-bottom:30px;">
              <div style="font-size:12px;color:#a78bfa;font-weight:800;letter-spacing:1px;text-transform:uppercase;margin-bottom:10px;">
                💬 Message Content:
              </div>
              <div style="color:#e2e8f0;font-size:15px;line-height:1.7;white-space:pre-wrap;font-family:inherit;">
{message}
              </div>
            </div>

            <!-- 3D Quick Action Reply Button -->
            <table width="100%" cellpadding="0" cellspacing="0">
              <tr>
                <td align="center">
                  <a href="mailto:{email}?subject=Re:%20{subject}" style="display:inline-block;padding:16px 36px;border-radius:50px;background:linear-gradient(135deg,#7c3aed,#6d28d9);color:#ffffff;font-size:15px;font-weight:800;text-decoration:none;letter-spacing:0.5px;box-shadow:0 10px 25px rgba(124,58,237,0.5), inset 0 1px 1px rgba(255,255,255,0.4);border:1px solid rgba(255,255,255,0.2);">
                    ✉️ Reply Directly to {name}
                  </a>
                </td>
              </tr>
            </table>

          </td>
        </tr>

        <!-- Footer -->
        <tr>
          <td style="padding:20px;background:#090d1a;text-align:center;border-top:1px solid rgba(255,255,255,0.06);">
            <p style="margin:0;font-size:12px;color:#64748b;font-weight:500;">
              Portfolio Lead Notification • Om Verma © 2026
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

        # ==========================================================
        # 3D EMAIL TEMPLATE 2: TO VISITOR (CONFIRMATION AUTO-REPLY)
        # ==========================================================
        reply_subject = "Thank You For Contacting Me 🚀"

        reply_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Thank You For Contacting Me</title>
</head>
<body style="margin:0;padding:0;background-color:#070B14;font-family:'Segoe UI',Roboto,Helvetica,Arial,sans-serif;-webkit-font-smoothing:antialiased;">
<table width="100%" cellpadding="0" cellspacing="0" style="background-color:#070B14;padding:40px 15px;">
  <tr>
    <td align="center">
      <!-- Outer 3D Card Shell -->
      <table width="100%" max-width="640" cellpadding="0" cellspacing="0" style="max-width:640px;background:#0d1326;border-radius:28px;border:1px solid rgba(139,92,246,0.35);box-shadow:0 35px 80px rgba(0,0,0,0.85), 0 0 50px rgba(139,92,246,0.25);overflow:hidden;">
        
        <!-- 3D Header Hero -->
        <tr>
          <td style="padding:50px 35px 40px 35px;background:linear-gradient(135deg,#4c1d95,#7c3aed,#06b6d4);text-align:center;border-bottom:1px solid rgba(255,255,255,0.15);">
            
            <!-- 3D Floating Icon Ring -->
            <div style="display:inline-block;width:72px;height:72px;line-height:72px;border-radius:24px;background:rgba(255,255,255,0.15);border:1px solid rgba(255,255,255,0.35);box-shadow:0 15px 35px rgba(0,0,0,0.4), inset 0 1px 2px rgba(255,255,255,0.5);margin-bottom:18px;font-size:36px;">
              🚀
            </div>

            <div style="display:block;margin-bottom:10px;">
              <span style="display:inline-block;padding:6px 16px;border-radius:30px;background:rgba(0,0,0,0.35);border:1px solid rgba(255,255,255,0.2);color:#38bdf8;font-size:12px;font-weight:800;letter-spacing:1.5px;text-transform:uppercase;">
                ● MESSAGE DELIVERED
              </span>
            </div>

            <h1 style="margin:0;color:#ffffff;font-size:34px;font-weight:900;letter-spacing:-0.5px;text-shadow:0 4px 20px rgba(0,0,0,0.5);">
              Thank You, {name}!
            </h1>
            <p style="margin:12px 0 0 0;color:#f3e8ff;font-size:16px;font-weight:500;">
              Your message has landed safely in my inbox.
            </p>
          </td>
        </tr>

        <!-- Card Body -->
        <tr>
          <td style="padding:35px 30px;">
            
            <p style="margin:0 0 20px 0;color:#cbd5e1;font-size:15px;line-height:1.8;">
              Hi <strong style="color:#ffffff;">{name}</strong>,<br>
              Thank you for reaching out through my portfolio! I have received your message and will carefully review it. You can expect a response back from me within <strong style="color:#a78bfa;">24–48 hours</strong>.
            </p>

            <!-- 3D Summary Box -->
            <div style="padding:20px;background:#131b35;border-radius:18px;border:1px solid rgba(255,255,255,0.08);box-shadow:inset 0 2px 5px rgba(0,0,0,0.4);margin-bottom:30px;">
              <div style="font-size:11px;color:#a78bfa;font-weight:800;letter-spacing:1px;text-transform:uppercase;margin-bottom:8px;">
                📨 Submitted Summary:
              </div>
              <div style="font-size:14px;color:#94a3b8;margin-bottom:6px;">
                <strong style="color:#e2e8f0;">Subject:</strong> {subject}
              </div>
              <div style="font-size:14px;color:#cbd5e1;line-height:1.6;font-style:italic;background:#0d1326;padding:12px 16px;border-radius:12px;border-left:3px solid #7c3aed;margin-top:10px;">
                "{message}"
              </div>
            </div>

            <!-- 3D Action Buttons Grid -->
            <div style="text-align:center;margin-bottom:10px;">
              <p style="margin:0 0 16px 0;color:#94a3b8;font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:1px;">
                Explore My Work & Connect:
              </p>
              <table width="100%" cellpadding="0" cellspacing="0">
                <tr>
                  <td align="center">
                    <a href="{portfolio_url}" style="display:inline-block;padding:12px 22px;border-radius:14px;background:#7c3aed;color:#ffffff;font-size:13px;font-weight:700;text-decoration:none;margin:5px;box-shadow:0 8px 20px rgba(124,58,237,0.4), inset 0 1px 1px rgba(255,255,255,0.3);border:1px solid rgba(255,255,255,0.15);">
                      🌐 Portfolio
                    </a>
                    <a href="https://github.com/Omverma713" style="display:inline-block;padding:12px 22px;border-radius:14px;background:#1e293b;color:#ffffff;font-size:13px;font-weight:700;text-decoration:none;margin:5px;box-shadow:0 8px 20px rgba(0,0,0,0.4), inset 0 1px 1px rgba(255,255,255,0.2);border:1px solid rgba(255,255,255,0.1);">
                      💻 GitHub
                    </a>
                    <a href="https://www.linkedin.com/in/om-verma-a4a098256/" style="display:inline-block;padding:12px 22px;border-radius:14px;background:#0284c7;color:#ffffff;font-size:13px;font-weight:700;text-decoration:none;margin:5px;box-shadow:0 8px 20px rgba(2,132,199,0.4), inset 0 1px 1px rgba(255,255,255,0.3);border:1px solid rgba(255,255,255,0.15);">
                      💼 LinkedIn
                    </a>
                    <a href="{resume_url}" style="display:inline-block;padding:12px 22px;border-radius:14px;background:#059669;color:#ffffff;font-size:13px;font-weight:700;text-decoration:none;margin:5px;box-shadow:0 8px 20px rgba(5,150,105,0.4), inset 0 1px 1px rgba(255,255,255,0.3);border:1px solid rgba(255,255,255,0.15);">
                      📄 Resume
                    </a>
                  </td>
                </tr>
              </table>
            </div>

            <!-- Divider -->
            <hr style="margin:30px 0;border:none;border-top:1px solid rgba(255,255,255,0.08);">

            <!-- Signature -->
            <table width="100%" cellpadding="0" cellspacing="0">
              <tr>
                <td>
                  <div style="font-size:14px;color:#94a3b8;">Warm regards,</div>
                  <div style="font-size:20px;font-weight:900;color:#ffffff;margin-top:4px;letter-spacing:-0.3px;">Om Verma</div>
                  <div style="font-size:13px;color:#a78bfa;font-weight:600;margin-top:2px;">Full Stack Developer • Django & React</div>
                </td>
              </tr>
            </table>

          </td>
        </tr>

        <!-- 3D Footer -->
        <tr>
          <td style="padding:22px;background:#090d1a;text-align:center;border-top:1px solid rgba(255,255,255,0.06);">
            <p style="margin:0;font-size:12px;color:#64748b;font-weight:500;">
              © 2026 Om Verma • Built with Django, React & Tailwind CSS
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

        # ==========================================================
        # NON-BLOCKING ASYNC EMAIL DISPATCH
        # ==========================================================
        # Run email delivery in a background daemon thread so user
        # experiences instant response (< 50ms) with zero waiting.
        threading.Thread(
            target=_send_emails_background,
            args=(name, email, subject, message, subject_line, html_message, reply_subject, reply_html),
            daemon=True,
        ).start()

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


def resume_view(request):
    return render(request, "main/resume_soon.html")


def uploading_soon(request):
    return render(request, "main/uploading_soon.html")


def live_demo_soon(request):
    return render(request, "main/live_demo_soon.html")


def github_soon(request):
    return render(request, "main/github_soon.html")

