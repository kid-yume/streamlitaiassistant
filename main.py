import streamlit as st
import numpy as np
from openai import OpenAI
from utilities.databse import DatabaseManager
from utilities.queries import THREAD_QUERY,RUN_QUERY
import time,json

#initialize objects so that they may be accessed later in code 

#Lets title it 
st.title("ChatGPT 3.5 Turbo Sample Chat App with Functions")


@st.cache_resource
def get_config():
    data ={}
    with open("./config.json", "r") as jsonfile:
        data = json.load(jsonfile)
        print("Read successfully")
        print(data)
    return data

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    #if no thread exists create one or pull one that is in database. 
    data=get_config()
    client = OpenAI(api_key=data["API_KEY"])
    dbm = DatabaseManager()
    if len(dbm.ExecuteQuery(THREAD_QUERY)) == 0:
        emptyThread = client.beta.threads.create()
        dbm.ExecuteInsert("INSERT INTO THREADS VALUES ('{}',{},'{}')".format(emptyThread.id,emptyThread.created_at,emptyThread.metadata))
        dbm.CloseConnection()
    else:
        #IF thread exists lets pull the thread and display all messages in UI for visibility 
        thread =dbm.ExecuteQuery(THREAD_QUERY)
        aiThread = client.beta.threads.retrieve(thread_id=thread['ID'][0])
        messages = client.beta.threads.messages.list(thread_id=aiThread.id,order="asc")
        for message in messages:
            messageContent = ""
            for messageValue in message.content:
                messageContent = messageContent+messageValue.text.value
            try:
                st.session_state.messages.index({"role": message.role, "content": messageContent,"ThreadID":aiThread.id})
            except:
                st.session_state.messages.append({"role": message.role, "content": messageContent,"ThreadID":aiThread.id})
        dbm.CloseConnection()

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        

#This code collects the User message. When they press Enter the magic begins 
prompt = st.chat_input("Say Something")
if prompt:
    data=get_config()
    client = OpenAI(api_key=data["API_KEY"])
    dbm = DatabaseManager()
    with st.chat_message("user"):
        st.markdown(prompt)

    #Lets check Chat History to see if we can just grab the ThreadID from a message if not Run A SQL Query for it.
    threadId=""
    if len(st.session_state.messages) > 0:
        threadId=st.session_state.messages[0]["ThreadID"]
    else:
        threadId=dbm.ExecuteQuery(THREAD_QUERY)
        threadId= threadId['ID'][0]

    #Now we can add the user message to the Message Stack.
    thread_message = client.beta.threads.messages.create(
        threadId,
        role="user",
        content="{}".format(prompt),
        )
    
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt,"ThreadID":threadId})
    
    #With Run we are basically signalling the Assistant to process The Thread and send a reply
    #We use the @thread_id from the thread we created. The assistant ID can be found in the openAI dashboard
    run = client.beta.threads.runs.create(
        thread_id=threadId,
        assistant_id=data["ASSITANT_ID"]
    )
    

    #We know wait for the RUN to process. if it goes into a "Requires Action" State Lets save it in database for processing 
    #We add a while loop to make it a blocking statement so no other moves will take place until we have a reply
    while run.status != "completed":
        if run.status == "requires_action":
            print("Awaiting for function to run for "+run.id)
            if len(dbm.ExecuteQuery(RUN_QUERY.replace("{RUNID}",run.id))) == 0:
                dbm.ExecuteInsert("INSERT INTO RUNS VALUES ('{}','{}','{}')".format(run.id,threadId,run.status))
            else:
                pass
        
        #update Run object so we know when the status is complete 
        run = client.beta.threads.runs.retrieve(
            run_id=run.id,
            thread_id=threadId
        )
        time.sleep(2)
    #Once updated we can pull the AI's response from the thread and populate or Chat UI
    aiThread = client.beta.threads.retrieve(thread_id=threadId)
    messages = client.beta.threads.messages.list(thread_id=aiThread.id,order="asc")
    for message in messages:
        messageContent = ""
        for messageValue in message.content:
            messageContent = messageContent+messageValue.text.value
        try:
            st.session_state.messages.index({"role": message.role, "content": messageContent,"ThreadID":aiThread.id})
        except:
            with st.chat_message(message.role):
                st.markdown(messageContent)
                st.session_state.messages.append({"role": message.role, "content": messageContent,"ThreadID":aiThread.id})
    dbm.CloseConnection()
    print("Completed")
      


#print(st.session_state.botmessages)
#thread_messages = Thread(target=print_even_numbers)
#add_script_run_ctx(thread_even)


#