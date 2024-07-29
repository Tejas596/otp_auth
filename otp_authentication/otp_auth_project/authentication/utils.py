import pyotp

def generate_otp(email):
    otp_secret = pyotp.random_base32()
    otp = pyotp.TOTP(otp_secret)
    otp_code = otp.now()
    return otp_secret, otp_code

def verify_otp(otp_secret, otp_entered):
    otp = pyotp.TOTP(otp_secret)
    return otp.verify(otp_entered)
    
def send_otp_email(email, otp_code):
    print(f"Sending OTP to {email}: {otp_code}")
