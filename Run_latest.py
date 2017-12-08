import csv
import random
import sched, time, threading
import string
from Read import getUser, getMessage
from Socket import openSocket, sendMessage
from Initialize import joinRoom

all_quiz=[]
user_point_dict={}
current_quiz_id=None
current_quiz_answer=''
current_question_ended=False
quiz_running = False
s = openSocket()
joinRoom(s)
readbuffer = ""
i=1


def init_quiz():
    global all_quiz
    quiz_running = True
    with open('quiz.csv', 'r') as f:
        reader = csv.reader(f)
        all_quiz = list(reader)


def reinit_globals():
    global user_point_dict, current_quiz_answer
    user_point_dict = {}
    current_quiz_answer = ''


def get_random_quiz():
    if len(all_quiz)<1:
        return None
    l= random.choice(all_quiz)
    all_quiz.remove(l)
    return l


def make_quiz_question(l):
    global current_quiz_answer
    global current_question_ended
    current_question_ended = False
    q = l[1]
    s= l[0]+" 1. {0}  2. {1} 3. {2}. 4. {3}".format(l[1],l[2],l[3],l[4])
    global current_quiz_answer
    current_quiz_answer = l[5]
    return s


def print_question():
    print make_quiz_question(val)
    



def thread_entry():
    global quiz_running
    global s
    sendMessage(s,'Starting Chess Triva in 10 seconds. Hold your Horses and Pawns!')
    time.sleep(10)
    while quiz_running:
        q = get_random_quiz()
        ##if no questin left
        if q is None:
            quiz_running = False
        else:
            sendMessage(s, make_quiz_question(q) )
            
            time.sleep(120)

            
        



def send_top():
    global user_point_dict
    global s
    st=''
    counter=0
    #print if not empty
    if user_point_dict :
        keys=key=sorted(user_point_dict, key=user_point_dict.get, reverse=True)
        for i in keys:
            counter += 1
            st= st+ str( counter)+'. ' + i + '('+ str(user_point_dict[i]) + ')  '
            if counter == 5:
                break
                
    sendMessage(s,st)
   
        
        
        
    

##check commands
def user_is_mod(user):
    return True



##check commands
def check_command(chat, user):
    global quiz_running
    global current_quiz_answer
    global current_question_ended
    global s
    print 'checking command: ', chat
    print 'right answer: ', current_quiz_answer
    
    if '!startQuiz' in chat:
        if user_is_mod(user):
            if quiz_running == False:
                init_quiz()
                quiz_running = True
                t=threading.Thread(target=thread_entry)
                t.setDaemon(True)
                t.start()
                print "Thread started"
    if '!stopQuiz' in chat:
        quiz_running = False
        reinit_globals()
        
    if '!top5' in chat:
        print 'Sending top'
        send_top()
    
    if quiz_running and not current_question_ended and current_quiz_answer and current_quiz_answer.lower() in chat.lower():
        ms = 'Correct answer by: ' + user
        current_question_ended = True
        sendMessage(s,ms)
        if user_point_dict.has_key(user):
            user_point_dict[user] = user_point_dict[user]+1
        else:
            user_point_dict[user] = 1
        



#running

while True:
        readbuffer = readbuffer + s.recv(1024)
        temp = string.split(readbuffer, "\n")
        readbuffer = temp.pop()
        i=i+1
        print i, len(temp), temp

        for line in temp:
                        
            if "PING" in line:
                s.send(line.replace("PING", "PONG") + "\r\n")
                break

            user = getUser(line)
            message = getMessage(line)
            check_command(message, user)
   
