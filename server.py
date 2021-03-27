from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import json

from twilio.rest import Client
account_sid = "AC167074f4e25d2880038fc09ecac46127"
auth_token  = "a519ca618c85ed83e6615a7a7e18422c"
client = Client(account_sid, auth_token)

'''
# What does this thing need to store
- Name of Owner
- Name of Helper
- Phone Number of Owner
- Phone Number of Helper
- Tasks+when they need to be done



employments = {
    "owner": {"name": Arjun", "phoneNumber": "-27xxxxxx"}, 
    "helper": {"name": Julie", "phoneNumber": "-27xxxxxx"},
    "tasks": [
        {"Name": "Wash Dishes", "Time": {"day": "Monday", "specificWeekInMonth": None}}, <- this means 
        {"Name": "Clean mess in entrance hall", "Time": None} <- this means do the next day / asap
    ],
    "todaysTasks": [{name: "whatever", complete: false}]
}
OWNER
#step 1: get first message from owner *store owner phone numer
#step 2: get name of owner *store owners name
#step 3: Send instructions on how to send us tasks
#step 4: recieve tasks and populate tasks list

HELPER
#step 3: send link to the helper
#step 3.1: *store helper phone number
#step 3.2: get helpers name *store name


#every day you are generating a list of tasks


    #pullup tasks, extract all the tasks for that day

    todaysTasks = [task1, task2]
    todaysTasks = [{name: "whatever", complete: false}]

    MessageToHelper = "Hi Julie, Here are your tasks for today: "
    for i in range(todaysTasks.size()):
        MessageToHelper = MessageToHelper + "\n " + 


    send message to Helper


    *wait for task ID

    e.g. we recieve 1

    Update the message with task 1 stroked out

    Optio0:
    Option1: store complete task index [1, 0] (neatest maybe)
    Option2: replace the task with none and create new list of tasks complete

    resend Message

tasks = {"Wash dishes": "Daily", "Wash Clothes": {"day": "Monday", "specificWeekInMonth": None}}
tasks = [
    {"Name": "Wash Dishes", "Time": {"day": "Monday", "specificWeekInMonth": None}}, <- this means 
    {"Name": "Clean mess in entrance hall", "Time": None} <- this means do the next day / asap
]
'''
#This is where I store my user data (need to figure out long term storage option)
employments = [{
    "owner": {"name": "Arjun", "phoneNumber": "+27814111333"}, 
    "helper": {"name": "Julie", "phoneNumber": "+27555"},
    "tasks": [{"task": "Wash Dishes", "time": {"day": "Monday", "week": None}},
        {"task": "Clean mess in entrance hall", "time": None}],
        "todaysTasks": [{"task": "whatever", "complete": False}]}, 
        {"owner": {"name": "Cameo", "phoneNumber": "+278000"},
        "tasks": []}]

#This class sends messages, recieves 
def send_message(phone_number, message):
    message = client.messages.create(
        to="whatsapp:" + phone_number,
        from_="whatsapp:+14155238886",
        body=message)
    print(message.sid)

def handle_incoming_message(phone_number, message):
    newText = setupBot(phone_number, message)
    send_message(phone_number, newText)
    
def get_user(phone_number):
    #we don't know who is contacting us so we find the index of the list based on the phonenumber
    index = 0
    found = False
    who = ""

    while(found == False and index<len(employments)):

        if(employments[index]["owner"]["phoneNumber"] == phone_number):
            found = True
            who = "owner"
        elif (employments[index]["helper"]["phoneNumber"] == phone_number):
            found = True
            who = "helper"
        else:
            index=index+1
            
    return index, who, found

def setupBot(phone_number, text_message):
    #For testing purposes:
    bot_message = ""
    index, who, found = get_user(phone_number)
    #do we have this phone number in our system? if no, we need to create a element in our database for them
    if(found == False):
            #The phone number does not exist in the database so we setup as a new user in the database
            employments.append({
                "owner": {"name": None, "phoneNumber": phone_number}, 
                "helper": {"name": None, "phoneNumber": None},
                "tasks": []
            })
            bot_message = "Welcome to helper-helper! You’re new here, aren’t you - \n\nWhat’s your name?\n\nIf you are not new please Contact Support @911"
    else:
        #Lets figure out who we are talking to
        if(who == "owner"):
            #lets check if we have the owners name
            if(employments[index][who]["name"] == None):

                employments[index]["name"] = text_message
                bot_message = "Great to meet you, "+text_message+"!\
                        \n\nLet’s help you help your helper to know exactly what needs doing🙂.\
                        \n\nFirst, we need to add your helper to this bot.\
                        \n\nPlease send your helper this link to click on:\
                        https://wa.me/14155238886/?text=help-14155238886\
                        \n\nWe’ll let you know when she successfully joins up.\
                        \n\nIn the meanwhile, you can begin messaging me to add new todo items onto your helpers list.\
                        \nYou can add recurring items, too! Here are some examples you can try:\
                        \n\n```Wash dishes every day\nMop bathrooms every monday\
                        \nWipe windows on the first tuesday of every month\nDo laundry on tuesdays\
                        \nDo laundry on thursdays\nClean the messy entrance hall```"
            else:
                #The only thing we need to do now is populate the list for them now
                if(text_message == "DONE"):
                    if(len(employments[index]["tasks"]) == 0):
                        bot_message = "We do not seem to have any tasks in your list"
                    else:
                        bot_message = "Thank you " + employments[index][who]["name"] + "\
                            \n\nYour helper will have her list ready tomorrow morning before she\
                            comes into work.\n\nText me anytime if you need to add a new task"
                else:
                    bot_message = "Thank you for this task, give me more!\
                        \n\nIf you have no tasks left for me to save just text DONE"
                    employments[index]["tasks"].append(text_message)

        elif(who == "helper"):
            print(who)
        else:
            print("We don't know who you are")

    return bot_message

def textSniffer(text_message):

    splitlines = text_message.splitlines()

    for task_line in splitlines:
        task_line.split(" ")

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps({
            'ayyyyy': 'lmao',
            'method': self.command,
            'path': self.path,
            'real_path': parsed_path.query,
            'query': parsed_path.query,
            'request_version': self.request_version,
            'protocol_version': self.protocol_version
        }).encode())
        return

    def do_POST(self):
        content_len = int(self.headers.get('content-length'))
        post_body = self.rfile.read(content_len)
        data = json.loads(post_body)
        print(data)
        parsed_path = urlparse(self.path)
        self.send_response(200)
        self.end_headers()
        phone_number = data["From"].split(":")[1]
        message = data["Body"]
        handle_incoming_message(phone_number, message)
        self.wfile.write(json.dumps({
            'method': self.command,
            'path': self.path,
            'real_path': parsed_path.query,
            'query': parsed_path.query,
            'request_version': self.request_version,
            'protocol_version': self.protocol_version,
            'body': data
        }).encode())
        return

if __name__ == '__main__':
    server = HTTPServer(('localhost', 8000), RequestHandler)
    print('Starting server at http://localhost:8000')
    server.serve_forever()