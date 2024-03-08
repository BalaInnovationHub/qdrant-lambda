from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer

qdrant = QdrantClient(":memory:") 

def handler(event,context):
    collections = event["queryStringParameters"]["collection"]
    question = event["queryStringParameters"]["question"]
    # Let's now search for something
    hits = qdrant.search(
        collection_name=collections,
        query_vector=encoder.encode(question).tolist(),
        limit=3
    )
    for hit in hits:
        result =+(hit.payload, "score:", hit.score)
        print(hit.payload, "score:", hit.score)
    return result
#fetch_vectors("sql-queries","Aliens attack our planet")