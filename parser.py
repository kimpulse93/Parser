import imaplib
import email.message
import os.path
import datetime
import xlrd

YA_HOST = "imap.yandex.ru"
YA_PORT = 993
YA_USER = ""
YA_PASSWORD = ""

pause_time = 5000


class Getmail():
    """ClientTask"""
    def __init__(self):
        self.id = 1

    def yandex(self,sender):

        # Connect and login
        imap = imaplib.IMAP4_SSL(YA_HOST)
        imap.login(YA_USER, YA_PASSWORD)
        status, select_data = imap.select()
        

        # From whom the letter
        status, search_data = imap.search(None, 'connect-support@yandex-team.ru', sender)

        for msg_id in reversed(search_data[0].split()):
            status, msg_data = imap.fetch(msg_id, '(RFC822)')
            
        # includes headers and alternative payloads
            mail = email.message_from_bytes(msg_data[0][1])

            if mail.is_multipart():
                filelist = []
                path = './xls/' + datetime.datetime.today().strftime("%d-%m-%Y") + '/'
                if not os.path.exists(path):
                    os.makedirs(path)
                for part in mail.walk():
                    content_type = part.get_content_type()
                    filename = part.get_filename()
                    if filename:
                        print(content_type)
                        print(filename)
                        if '.xls' in filename:
                            filelist.append(filename)
                            print('Закачали файл: ', filename)

                            with open(path+part.get_filename(), 'wb') as new_file:
                                new_file.write(part.get_payload(decode=True))
                break
        imap.expunge()
        imap.logout()
