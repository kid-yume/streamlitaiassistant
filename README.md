<!-- mdformat off(GitHub header) -->
OpenAI Assitant API Streamlit Chat Example 
======
<!-- mdformat on -->

<p align="center">
  <a href="#grabngo--">
    <img src="https://storage.googleapis.com/gngloaners/gnglogo.png" alt="Grab n Go Icon" />
  </a>
</p>

The OpenAI Assisstant API is the latest release from openAI and eventually how one will have to interact with agents. 

This repository was created to provide a complete example on how the process work with conversing with an agent using [Assistant API](https://platform.openai.com/docs/assistants/how-it-works)

For this example I tried to keep it as simple as possible, so using SQLite Database and python was what I chose to go with. This is not meant to be a production solution in the slightest. I would definitely suggest taking better security measures and allocating resources more properly.  However, it is meant to show you that the features of Threads and functioncalling is not only amazing but now its more scalable then ever!  

I also used ChatGPT3.5 Model to show that through function calling not only can i enable this AI to send Email but this model can now describe Images by leveraging a chatgpt4 model! Idk about you but that got me pretty excited.

The reason I used a database was just because, I wanted to kind of save the state of the application. So when you close and re run the app the conversation is saved. Now if you want a start a new conversation clear the *THREADS* table. Just showing the power of threads through this. Before saving a previous conversation with [chat.completions] API would have been a bit tricky. 


## Running the application
At Its base this application will run with just configuration to the config.json file. I will also provide an assistant to start off with that will automatically create the assistant for you and show you its ID. Going back to the config file; The key to each of these items is in the paranthesis following What it is: 	
* **[Assistant ID(ASSISTANT_ID)](https://platform.openai.com/assistants)** This can be found in the OpenAI Dashboard. I will also include some code that can automatically create the Assistant for you. ^_^ 
* **[OpenAI API Key(API_KEY)](https://platform.openai.com/api-keys)** You can find this in your OpenAI Dashboard as well. 
* **Database File Location(DATABASE_NAME)** Sqlite3 runs a bit differently now username or password required and it just stores a db file to your desired location(Put full file path here to avoid any issues.). **Again not meant to be a production solution ;)  

### Optional Keys to fill in and their purpose.
Keep in mind I originally did this for myself and have an SQL Database I was interacting with so I was using **pyodbc**. Since everybody may not have a SQL Database, Everybody can get a SQLite Database with ease! I also had a bit of trouble configure SQLite with pyodbc so I will include how to do that in this tutorial in case you prefer pyodbc and still want to just get a quick understanding of interacting with this API

* **[3rd Party Email Provider(EMAIL_API_KEY)](https://www.mailjet.com/?utm_term=mailjet&utm_campaign=240134763&utm_content=&utm_source=google&utm_medium=cpc&creative=284720571834&keyword=mailjet&matchtype=e&network=g&device=c&gad_source=1&gclid=CjwKCAiAu9yqBhBmEiwAHTx5p8b2yZ_JLxyMOvUtR-15YAqzox904CETtHlqFzbwZ9CiTsUhcJeI5BoC7bwQAvD_BwE)** I used mailjet just cause it was quick and easy. I also didnt really feel like dealing with port security and such to use another provider. However feel free to challenge yourself and put gmail or even your own in this project. ^_^
* **[3rd Party Email Provider(EMAIL_SECRET_KEY)](https://www.mailjet.com/?utm_term=mailjet&utm_campaign=240134763&utm_content=&utm_source=google&utm_medium=cpc&creative=284720571834&keyword=mailjet&matchtype=e&network=g&device=c&gad_source=1&gclid=CjwKCAiAu9yqBhBmEiwAHTx5p8b2yZ_JLxyMOvUtR-15YAqzox904CETtHlqFzbwZ9CiTsUhcJeI5BoC7bwQAvD_BwE)** Mailjet requires your API and Secret to be used 

* **[Host Name(SERVER_HOSTNAME)]()** I used the hostname for mainly a pyodbc set-up since one has to include the FQDN of computer when connecting to the database 


### Creating the AI Assisstant. 
You have two options. You can create an Assistant through the [dashboard](https://platform.openai.com/assistants) or you can run the **create_assistants.py** file with 
```
python ./utilities/create_assistants.py
```
from the root of the folder. It includes the sample function calls as well if you run the code otherwise you would have to manually copy and paste them through the dashboard. These are functions that are meant to be used with the chat application. If your Assistant does not have them it will not break the application you will just get an undesired response when you ask it to analyze an image or send an email.


### Installing SQLite3 
 I would suggest using [homebrew]() to install SQLlite3 if you dont have it go ahead and download it. Otherwise run 
 ```
 brew install sqlite
 ```
 If you come across driver issues install from [here](http://www.ch-werner.de/sqliteodbc/) the driver worked great for me and they are great developers who ever did this. if your using pyodbc update your **odbcinst.ini** (mine was located /usr/local/etc/odbcinst.ini)file and add the following line 
 ```
[SQLite3 Driver]
Driver = /usr/local/lib/libsqlite3odbc.dylib
Description=Microsoft ODBC Driver 17 for SQL Server
UsageCount=1
 ```
 Then in pyodbc use 
 ```
 
 ```

Download or pull the repository from the root of the directory run 
```
streamlit run main.py
```