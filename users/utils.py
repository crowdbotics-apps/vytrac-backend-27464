from django.core.mail import EmailMessage


import threading


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.content_subtype = 'html'
        self.email.send()


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        EmailThread(email).start()
      # temp-mail.org : fake emails site for expermenting
      # _____ note:
      # This may don't work untill you edite the setting of your google email account of the company
      # Steps
        # 1) go to https://www.google.com/settings/security/lesssecureapps
        # 2) Allow less secure apps: OFF => Allow less secure apps: ON
      # for more about the topic please
      # visit https://stackoverflow.com/questions/16512592/login-credentials-not-working-with-gmail-smtp
