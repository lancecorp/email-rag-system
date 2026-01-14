class Index:
    index_name = "emails_vector_index"

    index_body = {
        "settings": {
            "index.knn": True,
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "properties": {
                "id": {"type": "keyword"},
                "text": {"type": "text"},
                "embedding": {
                    "type": "knn_vector",
                    "dimension": 384,
                    "method": {
                        "name": "hnsw",
                        "space_type": "cosinesimil",
                        "engine": "lucene"
                    }
                }
            }
        }
    }

    # Example Groq-style query
    query_body = {
        "size": 10,
        "query": {
            "knn": {
                "embedding": {
                    "k": 10
                }
            }
        }
    }