# ceng-407-408-2022-2023-Turkish-ChatBot-System-for-Cankaya-University-using-Artificial-Intelligence
Turkish ChatBot System for Cankaya University using Artificial Intelligence

### Installation Instructions:

**GPT3 MODEL AND BERT MODEL**

- If you want to use ChatbotTelegramBot and ChatbotWebApp you must run backend.py first.

- For GPT3 Model, ask contributors for OpenAI key(openai.api_key = "write Openai api key here"), and set the your model in here(model="write trained gpt3 model name here")

- For Bert Model, you should download Elasticsearch first. Download here : https://www.elastic.co/downloads/elasticsearch 
After downloading Elasticsearch, a zip file named elasticsearch-8.8.1-windows-x86_64 will download to your computer. Extract this zip file to the directory in your folder where you are sure that you have more than 64GB free space on your computer. Go to this folder on your computer and run bin/elasticsearch.batch file respectively (Example: C:\Users\Hpi5-9\elasticsearch-8.8.1\bin). After running this file, Elasticsearch will start to install on your computer and you will be able to see your password in the window that opens. After copying your password, enter your password instead of the password in the backend.py file ( http_auth=('elastic', 'write elastic password here'),). !!!Do not close batch file while running backend.py.

  
**Chatbot Telegram Bot:**

- Visit the Telegram app on your device.

- Search for "Turkish Chatbot System" and select the bot or you can just click the link : 
https://t.me/TurkishCankayaChatbot

- Follow the on-screen instructions to choose the desired model and type your questions.

- You can also ask questions via voice message. 

**Cankaya University Web App:**

- Clone Github Repo to your local computer (https://github.com/CankayaUniversity/ceng-407-408-2022-2023-Turkish-ChatBot-System-for-Cankaya-University-using-Artificial-Intelligence.git) .

- Go to ChatbotComparison directory.

- Type` npm run install `on your terminal.

- Type` npm run dev `on your terminal.

- This command will open your web browser and navigate to the Chatbot web app.

-  You can ask questions while browsing the site .

**Cankaya University Mobile App:**

- Click the link for download the apk (https://github.com/CankayaUniversity/ceng-407-408-2022-2023-Turkish-ChatBot-System-for-Cankaya-University-using-Artificial-Intelligence/blob/main/CankayaChatBotApp/app-debug.apk)

### Usage Examples:

**Chatbot Telegram Bot:**

[voice message] - Send a voice message to transcribe and receive a text-based answer
[text message] - Type and send a text-based question to receive an answer

|![image](https://github.com/CankayaUniversity/ceng-407-408-2022-2023-Turkish-ChatBot-System-for-Cankaya-University-using-Artificial-Intelligence/assets/76754183/06db54ee-b879-465a-9593-b12b4e3bf814)|
|:--:| 
| Figure1: TelegramBot user interface & example usage|

**Chatbot Web App:**

[text message] - Type and send a text-based question to receive an answer

|![maaaa2](https://github.com/CankayaUniversity/ceng-407-408-2022-2023-Turkish-ChatBot-System-for-Cankaya-University-using-Artificial-Intelligence/assets/76754183/0210e0ca-436e-4a56-9130-e0a38ca8cb7d)|
|:--:| 
| Figure2: Chatbot classifier user interface & example usage |

**Chatbot Android App:**

[text message] - Type and send a text-based question to receive an answer

|![chat](https://github.com/CankayaUniversity/ceng-407-408-2022-2023-Turkish-ChatBot-System-for-Cankaya-University-using-Artificial-Intelligence/assets/76754183/51ace9f4-d6ab-46cd-bafb-82dbdbb83881)|
|:--:| 
| Figure3: Chatbot Android Application user interface & example usage |
