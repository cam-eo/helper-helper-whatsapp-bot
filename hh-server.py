from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import json

app = Flask(__name__)

employments = [{
    "owner": {"name": "Arjun", "phoneNumber": "+27814111333"}, 
    "helper": {"name": "Julie", "phoneNumber": "+27555"},
    "tasks": [
        {"task": "Wash Dishes", "time": {"date": "Monday", "specificWeekInMonth": None}}, 
        {"task": "Clean mess in entrance hall", "time": None}],
        "todays_tasks": [
            {"name": "whatever", "complete": False}]}, 
            {"owner": {"name": "Cameo", "phoneNumber": "+278000"},
            "helper": {"name": None, "phoneNumber": None},
            "tasks": []}]

@app.route("/", methods=['POST', 'GET'])
def response_handle():
    """Respond to incoming whatsapp messages"""
    # Fetch the message
    text_message = request.form.get('Body')
    #Fetch the phone number
    phone_number = request.form.get('From').split(":")[1]
    print(phone_number)

    # Create reply
    resp = MessagingResponse()
    resp.message(helper_bot(phone_number, text_message))


    return str(resp)


def get_user(phone_number):
    #we don't know who is contacting us so we find the index of the list based on the phone_number
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

def task_sniffer(text_message):
    text_lines = text_message.split(" ")
    print(text_lines)


def helper_bot(phone_number, text_message):
    #For testing purposes:
    bot_message = ""
    index, who, found = get_user(phone_number)
    print(text_message)
    #do we have this phone number in our system? if no, we need to create a element in our database for them
    if(found == False):
        """
        The phone number does not exist in the database so we setup as a new user in the database
        We need to determine if this is an owner or a helper setting up
        """
        #if this is a helper setup message. Add the helper to the appropriate owner number
        text_split = text_message.split("-")
        if(text_split[0] == "helper"):
            owner_number = str(text_split[2]).replace(" ", "+")
            index, who, found = get_user(owner_number)
            # print("My Boss Is: "+employments[index]["owner"]["name"])
            employments[index]["helper"]["phoneNumber"] = phone_number
            print(employments[index]["helper"]["phoneNumber"])
            bot_message = "Welcome to ousie! You’re new here, aren’t you - \n\nWhat’s your name?"
        else:
            print("new owner found")
            employments.append({
                "owner": {"name": None, "phoneNumber": phone_number}, 
                "helper": {"name": None, "phoneNumber": None},
                "tasks": []
            })
            bot_message = "Welcome to helper-helper! You’re new here, aren’t you - \n\nWhat’s your name?"

    else:
        #Lets figure out who we are talking to
        if(who == "owner"):
            #lets check if we have the owners name
            if(employments[index][who]["name"] == None):
                employments[index][who]["name"] = text_message
                
                bot_message = "Great to meet you, "+text_message+"!\
                        \n\nLet’s help you help your helper to know exactly what needs doing🙂.\
                        \n\nFirst, we need to add your helper to this bot.\
                        \n\nPlease send your helper this link to click on:\
                        https://wa.me/14155238886/?text=helper-14155238886-"+phone_number+"\
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

            if(employments[index][who]["name"] == None):
                #we need to save the helpers details with the corresponding home owner
                employments[index][who]["name"] = text_message
                bot_message = "Great to meet you, "+text_message+"!\
                \n\nI will send you your list of tasks first thing in the morning🙂"
            else:
                bot_message = "Your Task List for Tomorrow is"
        else:
            print("We don't know who this is but we have this phone number")

    return bot_message


if __name__ == "__main__":
    app.run(debug=True)