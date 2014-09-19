import smtplib
from email.mime.text import MIMEText

def send_email(file, args):
    file = open(file, 'r')
    
    #parse the file and replace all entries denoted * text * with the value contained in the args dict
    line = file.readline()
    line_num = 0
    msg = ''

    while line:
        strs = line.split('*')
        
        #length of 'strs' should be odd to ensure that all * * pairs are closed
        if len(strs) % 2 != 1:
            raise Exception("expected '*' on line"+line_num)
        
        i = 0
        while i < len(strs):
            if i % 2 == 1:
                arg_key = strs[i].strip(' ') 
                arg_val = args[arg_key]
                msg += arg_val
            else:
                msg += strs[i]
            
            i += 1
        
        line_num += 1
        line = file.readline()

    msg = MIMEText(msg)
    file.close()
    
    msg['Subject'] = args['Subject']
    msg['From'] = args['From']
    msg['To'] = args['To']
    
    s = smtplib.SMTP('ssg-test')
    s.sendmail(msg['From'], [msg['To']], msg.as_string())
    s.quit()


def send_first_warning_email(username, user_email, list_name):
    send_email('list_app/email/first_warning.txt', {
            'Subject': 'Mailing List Expiration',
            'From': 'admin@ssg-test.nws.oregonstate.edu',
            'To': user_email,
            'owner_name': username,
            'link_addr': 'ssg-test.nws.oregonstate.edu',
            'list_name': 'list_name'
        })


def send_final_warning_email(user_name, list_name):
    send_email('list_app/email/first_warning.txt', {
        'Subject': 'Mailing List Expiration',
        'From': 'admin@ssg-test.nws.oregonstate.edu',
        'To': user_email,
        'owner_name': username,
        'link_addr': 'ssg-test.nws.oregonstate.edu',
        'list_name': 'list_name'
    })


def send_onid_transition_email(username):

def send_non_onid_transition_email(username):


def test():
    send_email('list_app/email/first_warning.txt', {
            'owner_name': 'wasingej',
            'list_name': 'ph_212',
            'link_addr': 'google.com'
        })
