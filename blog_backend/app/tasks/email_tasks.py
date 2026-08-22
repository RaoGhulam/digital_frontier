import resend

from app.core.config import settings


def send_verification_email(
    email: str,
    verification_url: str,
):
    resend.api_key = settings.RESEND_API_KEY

    params = {
        "from": "Digital Frontier <digital_frontier@resend.dev>",
        "to": [email],
        "subject": "Verify your email address",
        "html": f"""
            <h1>Verify your email</h1>

            <p>Thanks for creating an account.</p>

            <p>
                Click the button below to verify your email address:
            </p>

            <p>
                <a href="{verification_url}">
                    Verify my email
                </a>
            </p>

            <p>
                This link expires in 30 minutes.
            </p>
        """,
    }

    return resend.Emails.send(params)
