import datetime
import jwt
from django.core.mail import send_mail
from config.settings import SECRET_KEY
from datetime import datetime, timedelta, timezone

access_secret = SECRET_KEY
refresh_secret = SECRET_KEY

def create_token(user_id):
    access_payload = {
        'user_id':user_id,
        'type':'access',
        'exp':datetime.now(timezone.utc) + timedelta(minutes=60)
    }


    refresh_payload = {
        'user_id': user_id,
        'type': 'refresh',
        'exp': datetime.now(timezone.utc) + timedelta(minutes=150)
    }


    access = jwt.encode(access_payload,access_secret,algorithm='HS256')
    refresh = jwt.encode(refresh_payload,access_secret,algorithm='HS256')
    return access,refresh


if __name__ == '__main__':
    print(create_token(1))


def verify_token(token,secret,type='access'):
        try:
            payload = jwt.decode(token,access_secret,algorithms=['HS256'])
            if payload['type'] != type:
                return None
            return payload
        except jwt.ExpiredSignatureError:
            return 'token Expired'
        except  jwt.InvalidTokenError:
            return 'invalid token error'



if __name__ == '__main__':
    print(verify_token('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ0eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ4OTQ2OTcxfQ.6XCBklQ2roe98xtu-LqnauWPvuGuUcYTaCL1GZd3sgI', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ0eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0ODk0Njk3MX0.Hp4kRTt7a2qA-tZTyyqBzFTcmv9besQpR4YlnfahrUE'))



def refresh_token(refresh_token):
    payload = verify_token(refresh_token,refresh_secret,type='refresh')

    if not isinstance(payload,dict):
        return {'error':payload}

    access_payload = {
        'user_id':payload['user_id'],
        'type': 'access',
        'exp': datetime.now(timezone.utc) + timedelta(minutes=5)
    }

    access = jwt.encode(access_payload,access_secret,algorithm='HS256')
    return {'access':access}






def send_email(subject, message, to_email):
        send_mail(subject=subject,
                  message=message,
                  from_email='utkurovikromjon0@gmail.com',
                  recipient_list=[to_email],
                  fail_silently=True
                  )


