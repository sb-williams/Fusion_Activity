def send_message(is_activity, subject, body):

    import smtplib
    from email.mime.text import MIMEText

    print("Sending email")

    if is_activity == True:

        # Set up the message to be sent
        html2 = '''\
            <html>
            <head></head>
            <body>
            <p>**** THIS IS AN AUTOMATED MESSAGE ****<br>
            </p>
            '''

        html3 = '''\
            </body>
            </html>
            '''

        html = html2 + body + '<br>' + html3
        msg = MIMEText(html, 'html')
        msg['Subject'] = subject

        sender = 'no-reply@bpu.com'
        recipients = ["sbwilliams@bpu.com", "fusionjobs@bpu.com"]
        msg['From'] = sender
        msg['To'] = ", ".join(recipients)
        server = smtplib.SMTP('smtp.corp.bpu.local')
        server.sendmail(sender, recipients, msg.as_string())
        server.close()

        return True

    else:

        # Set up the message to be sent
        html2 = '''\
            <html>
            <head></head>
            <body>
            <p>**** THIS IS AN AUTOMATED MESSAGE ****<br>
            </p>
            '''

        html3 = '''\
            </body>
            </html>
            '''

        html = html2 + body + '<br>' + html3
        msg = MIMEText(html, 'html')
        msg['Subject'] = subject

        sender = 'no-reply@bpu.com'
        recipients = ["TableauDev@bpu.com", "fusionjobs@bpu.com"]
        msg['From'] = sender
        msg['To'] = ", ".join(recipients)
        server = smtplib.SMTP('smtp.corp.bpu.local')
        server.sendmail(sender, recipients, msg.as_string())
        server.close()

        return True

