RAG Email Code is using aol server to read data using **sentence-transformers/all-MiniLM-L6-v2** embedding model.
Deploy Docker using docker-compose.yml file.
Create .env file with below parameters:
IMAP_SERVER="imap.aol.com"
EMAIL_USER_NAME=
EMAIL_USER_PASSWORD=
DOCKER_USER_NAME=
DOCKER_USER_PASSWORD=
MODEL_NAME="sentence-transformers/all-MiniLM-L6-v2"
DOCKER_HOST=
DOCKER_PORT=
Install requirements.txt file.
Execute ingest_data.py first to fetch email data from aol server, create index and then map email data into the index. This will create a vector database in opensearch.
Finally execute app.py file. This will open streamlit in browser.
The email data ingested in Opensearch is related to offer, discount, sale and buy.
You can search these keys in Streamlit text input.
