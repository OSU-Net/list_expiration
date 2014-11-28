import smtplib
from email.mime.text import MIMEText
import pdb

#######################################################################################
#
# send text specified in 'file' as an email
# file(string): location of a template file containing the text for an email.  Entries
#               denoted '*entry*' will be replaced with the value for 'args[entry]'
#
# args(dict):   contains values for template entries.  In addition, must contain values 
#               'Subject', 'From' and 'To'
#
######################################################################################
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
    
    s = smtplib.SMTP('localhost')
    s.sendmail(msg['From'], [msg['To']], msg.as_string())
    s.quit()


def send_first_warning_email(user_email, list_name, link_addr):
    send_email('list_app/email/first_warning.txt', {
        'Subject': 'Mailing List Expiration',
        'From': 'admin@ssg-test.nws.oregonstate.edu',
        'To': user_email,
        'owner_email': user_email,
        'link_addr': link_addr,
        'list_name': list_name
    })


def send_final_warning_email(user_email, list_name, link_addr):
    send_email('list_app/email/first_warning.txt', {
        'Subject': 'Mailing List Expiration: Final Warning',
        'From': 'admin@ssg-test.nws.oregonstate.edu',
        'To': user_email,
        'owner_name': user_email,
        'link_addr': link_addr,
        'list_name': list_name
    })


def send_onid_transition_email(user_email, link_addr):
    send_email('list_app/email/onid_transition.txt', {
        'Subject': 'Notice to Mailing List Owners',
        'From': 'admin@ssg-test.nws.oregonstate.edu',
        'To': user_email,
        'owner_name': user_email,
        'link_addr': link_addr
    })

def send_non_onid_transition_email(owner_email, link_addr):
    send_email('list_app/email/non_onid_transition.txt', {
        'Subject': 'Notice to Mailing List Owners',
        'From': 'admin@ssg-test.nws.oregonstate.edu',
        'To': owner_email,
        'owner_name': owner_email,
        'link_addr': link_addr
    })
