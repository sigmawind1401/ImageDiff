import re
import dns.resolver
import socket
import smtplib

def check_mail_address(mail_add):

    # ドメインチェック
    mail_domain = re.search("(.*)(@)(.*)", mail_add).group(3)
    try:
        records  = dns.resolver.query(mail_domain, 'MX')
        mxRecord = records[0].exchange
        mxRecord = str(mxRecord)        
    except Exception as e:
        return False

    # メールアドレス存在チェック
    local_host = socket.gethostname()
    server = smtplib.SMTP(timeout=5)
    server.set_debuglevel(0)

    try:
        server.connect(mxRecord)
        server.helo(local_host)
        server.mail('test@example.com')
        code, message = server.rcpt(str(mail_add))
        server.quit()

        if code == 250:
            return True
        else:
            return False
    except Exception as e:
        return False