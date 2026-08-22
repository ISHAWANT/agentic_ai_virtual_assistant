### Agentic Ai Virtual Assistant

#### Create Virtual Enviroment

```bash 
conda create -p venv python==3.11 -y 

``` 

#### Install the packages from req.txt 

```bash 
pip install -r requirements.txt
``` 


#### Create a .env and added below secrets key

```bash 
TAVILY_API_KEY = "*****************"

WEATHERSTACK_API_KEY = "*****************" 

OPENAI_API_KEY = "*****************"

OPENAI_BASE_URL = "*****************"
``` 

#### Run the app.py file 

```bash 
streamlit run app.py 
``` 