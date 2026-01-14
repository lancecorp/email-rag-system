from sentence_transformers import SentenceTransformer
from opensearchpy import OpenSearch
from opensearchpy.helpers import bulk
from index import Index
from fetch_email import FetchEmail
from load_environment import LoadEnvironment
import nltk
import ssl
import time
import platform


class IngestData:

    @staticmethod
    def disable_ssl_certificate():

        print("Disabling SSL Certification for MAC OS")

        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context
        nltk.download("punkt_tab")

    @staticmethod
    def ingest_data():

        print("Data Ingestion Started")

        # Disable SSL Certificate Verification. Applicable for MAC.
        if platform.system() == "Darwin":
            IngestData.disable_ssl_certificate()

        # Create Sentence Embedding Model
        model = SentenceTransformer(LoadEnvironment.MODEL_NAME)
        print("Loaded Transformer Model =", model)

        # Create an OpenSearch Client with Authentication, SSL and Retry Settings.
        client = OpenSearch(
            hosts=[{"host": LoadEnvironment.DOCKER_HOST, "port": LoadEnvironment.DOCKER_PORT}],
            http_auth=(LoadEnvironment.DOCKER_USER_NAME, LoadEnvironment.DOCKER_USER_PASSWORD),
            use_ssl=True,
            verify_certs=False,
            ssl_show_warn=False,
            timeout=60,
            max_retries=3,
            retry_on_timeout=True
        )
        print("Client Connection to OpenSearch =", client.info())

        # Checking if Index Already Exists or Create a New Index
        if not client.indices.exists(index=Index.index_name):
            client.indices.create(index=Index.index_name, body=Index.index_body)
            print("Index created.")
        else:
            print("Index already exists.")

        # Fetching Email Data to Map it with Index
        print("Fetching Email Data")
        email_data = FetchEmail.fetch_email(LoadEnvironment.EMAIL_USER_NAME, LoadEnvironment.EMAIL_USER_PASSWORD)

        # Initialize Bulk Data
        actions = []
        # Loop through Emails with IDs
        print("Looping Through Emails to Create OpenSearch Document")
        for seq_num, email in enumerate(email_data, start=1):
            # Extract Each Email Body Text
            text = email["body"]
            # Generate Embedding Vector
            embedding_vector = model.encode(text).tolist()
            # Clean NaN Values
            embedding_vector = [0.0 if x != x else x for x in embedding_vector]
            # Create OpenSearch Bulk Document
            actions.append({
                "_index": Index.index_name,
                "_id": seq_num,
                "_source": {
                    "id": str(seq_num),
                    "text": text,
                    "embedding": embedding_vector
                }
            })

            # Divide Large Batch
            if seq_num % 50 == 0:
                bulk(client, actions)
                actions = []
                time.sleep(0.5)

        # Insert Remaining Email Body
        if actions:
            bulk(client, actions)

        print("Email Data Successfully Ingested in Vector Database")

# Execute Data Ingestion
if __name__ == "__main__":
    IngestData.ingest_data()