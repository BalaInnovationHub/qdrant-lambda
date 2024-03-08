from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer


# Let's make a semantic search for Sci-Fi books! 
documents = [
    {
        "Question": "What is my last 6 months sales",
        "SQLQuery": """ /*As the number of days(6*30=180) is greater than 45 days showing monthly sales*/SELECT MONTH(sale_date) As 'Month', SUM(sale_price) AS 'Sum of Monthly Sales' FROM Sales  WHERE sale_date >= DATEADD(MONTH, DATEDIFF(MONTH, 0, GETDATE()) - 6, 0)
  AND sale_date <  DATEADD(MONTH, DATEDIFF(MONTH, 0, GETDATE()), 0)   GROUP BY MONTH(sale_date)""",
    },
    {
        "Question": "list my invoice sales for the last month",
        "SQLQuery": """ /*As the number of days(30) is less than 45 days showing daily sales*/ SELECT FORMAT(sale_date,'MM-dd-yy') As 'Day Of Month', SUM(sale_price) AS 'Sum of Daily Sales' FROM Sales  WHERE sale_date >= DATEADD(MONTH, DATEDIFF(MONTH, 0, GETDATE()) - 1, 0)
  AND sale_date < DATEADD(MONTH, DATEDIFF(MONTH, 0, GETDATE()), 0)  GROUP BY sale_date ORDER BY sale_date"""
    }]

def handler(event,context):
    collections = event["queryStringParameters"]["collection"]
    queries = event["queryStringParameters"]["queries"]
    emb = event["queryStringParameters"]["emb"]
    encoder = SentenceTransformer(emb)
    qdrant = QdrantClient(":memory:") 
        # Create collection to store books
    qdrant.recreate_collection(
        collection_name=collections,
        vectors_config=models.VectorParams(
            size=encoder.get_sentence_embedding_dimension(), # Vector size is defined by used model
            distance=models.Distance.COSINE
        )
    )
    # Let's vectorize descriptions and upload to qdrant
    qdrant.upload_records(
        collection_name=collections,
        records=[
            models.Record(
                id=idx,
                vector=encoder.encode(doc["description"]).tolist(),
                payload=doc
            ) for idx, doc in enumerate(documents)
        ]
    )
    print("emb created")
    return "success"


def fetch_vectors(collections,question):
    # Let's now search for something
    hits = qdrant.search(
        collection_name=collections,
        query_vector=encoder.encode(question).tolist(),
        limit=3
    )
    for hit in hits:
        result =+(hit.payload, "score:", hit.score)
    return result

#add_sqlqueries("sql-queries",documents,'BAAI/bge-large-zh-v1.5')
#fetch_vectors("sql-queries","Aliens attack our planet")