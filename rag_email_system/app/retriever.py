from langchain_huggingface import HuggingFaceEmbeddings
from opensearchpy import OpenSearch
from load_environment import LoadEnvironment
from index import Index

class Retriever:

    @staticmethod
    def answer(query):

        # Hugging Face embeddings wrapper for LangChain to Convert Text into Vectors
        hf_embeddings = HuggingFaceEmbeddings(model_name=LoadEnvironment.MODEL_NAME)
        print("Hugging Face Embeddings Wrapper =", hf_embeddings)

        # Convert a Natural Language Query into Numeric Vector Embedding that can be Used for Sematic Search in Vector Database
        query_vector = hf_embeddings.embed_query(query)
        print("Query Vector =", query_vector)

        # Create Connection to OpenSearch Cluster
        client = OpenSearch(
            hosts=[{"host": LoadEnvironment.DOCKER_HOST, "port": LoadEnvironment.DOCKER_PORT}],
            http_auth=(LoadEnvironment.DOCKER_USER_NAME, LoadEnvironment.DOCKER_USER_PASSWORD),
            use_ssl=True,
            verify_certs=False
        )
        print("Client Connection = ", client.info())
        # Retrieve Mapping of an OpenSearch Index
        res = client.indices.get_mapping(index=Index.index_name)
        print("Index Mapping =", res)

        # Setting Query Vector in Index Query Body
        print("Setting Query Vector in Index Query Body")
        Index.query_body["query"]["knn"]["embedding"]["vector"] = query_vector

        # Execute a Search Query on OpenSearch Index
        res = client.search(index=Index.index_name, body=Index.query_body)
        print("Search Query Response =", res)

        # Retrieve Document Text
        content = "\n\n\n".join(text["_source"]["text"] for text in res["hits"]["hits"])
        print("Retrieve Document Text =", content)

        return content
