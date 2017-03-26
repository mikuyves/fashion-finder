# -*- coding: utf-8 -*-
#!/usr/bin/env python
import os
import re

from gmail import GMail, Message

from secret import BASEPATH, GMAIL_ACCOUNT, GMAIL_PASSWD, MAIL_TO



mail_to = MAIL_TO


def checkfolder():
    folders = []
    for folder, sub, filenames in os.walk(BASEPATH):
        if u'ready_to_send.gml' in filenames:
            folders.append(folder)
    return folders


def get_content(path, filenames, suffix):
    target_file = [f for f in filenames if re.search(suffix, f)][0]
    with open(os.path.join(path, target_file)) as f:
        file_content = f.read()
    return file_content


def sendmail(title, text, attachments):
    gmail = GMail(GMAIL_ACCOUNT, GMAIL_PASSWD)
    msg = Message(title,
                    to=mail_to,
                    text=text,
                    attachments=attachments
    )
    gmail.send(msg)
    gmail.close()


def main():
    folders = checkfolder()
    for folder in folders:
        for path, sub, filenames in os.walk(folder):
            try:
                title = get_content(path, filenames, 'flk$')
                text = get_content(path, filenames, 'txt$')
            except IndexError as e:
                print 'File with the suffix not found. Error: e' % e

            attachments = []
            for filename in filenames:
                attachment = os.path.join(path, filename)
                attachments.append(attachment)

            print 'Sending %s' % path
            sendmail(title, text, attachments)
            os.rename(
                os.path.join(path, 'ready_to_send.gml'),
                os.path.join(path, 'sent.gml')
            )
            print 'DONE!'


if __name__ == '__main__':
    main()
