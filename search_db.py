from typing import Optional
from pydantic import BaseModel
from crewai import Agent, Task, Crew, Process
from typing import List, Dict
from typing import Tuple, List, Dict, Any
import openai
from pymilvus import MilvusClient

from typing import Optional
from pydantic import BaseModel

def semantic_search(
    query_text: str,
    collection_name: str = "text_embeddings",
    milvus_file: str = "milvus_demoo.db",
    openai_api_key: str = "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"
) -> Tuple[List[Dict[str, Any]], str]:
    """
    Search function that generates OpenAI embeddings for query text and 
    performs semantic search in Milvus database using COSINE similarity.
    
    Args:
        query_text: Text to search for
        collection_name: Name of the Milvus collection
        milvus_file: Path to Milvus db file
        openai_api_key: OpenAI API key
    
    Returns:
        Tuple containing:
        - List of dictionaries with search results
        - Formatted string of search results
    """
    # Set OpenAI API key
    if openai_api_key:
        openai.api_key = openai_api_key
    
    # Generate embedding for query text
    try:
        response = openai.embeddings.create(
            model="text-embedding-3-small",
            input=query_text,
            encoding_format="float"
        )
        query_vector = response.data[0].embedding
    except Exception as e:
        raise Exception(f"Error generating OpenAI embedding: {str(e)}")
    
    # Initialize Milvus client and perform search
    try:
        client = MilvusClient(milvus_file)
        search_params = {
            "metric_type": "COSINE",
            "params": {"nprobe": 10}
        }
        
        print(f"Performing vector search for query: '{query_text}'...")
        results = client.search(
            collection_name=collection_name,
            data=[query_vector],
            limit=10,
            output_fields=["text", "conversation_id"],
            search_params=search_params
        )
        
        print(f"Search completed. Processing results...")
        
    except Exception as e:
        raise Exception(f"Error performing Milvus search: {str(e)}")
    
    # Process results into list of dictionaries
    search_results = []
    
    # Process results - assuming results[0] contains matches for our query vector
    if results and len(results) > 0:
        for hit in results[0]:  # results[0] contains the matches for our single query
            # Debug print to see the structure
            print(f"Processing hit: {hit}")
            
            search_result = {
                'id': hit['id'],
                'distance': float(hit['distance']),
                'similarity_score': 1 - float(hit['distance']),
                'text': hit['entity']['text'],
                'conversation_id': hit['entity']['conversation_id']
            }
            search_results.append(search_result)
            
            # Print individual results as they're processed
            print(f"\nDistance: {search_result['distance']}")
            print(f"Text: {search_result['text']}")
            print(f"Conversation ID: {search_result['conversation_id']}")
    
    # Create formatted string output
    output = f"Search Query: {query_text}\n\n"
    output += "Top 10 Most Similar Results:\n\n"
    
    for i, result in enumerate(search_results, 1):
        output += (
            f"Result #{i}:\n"
            f"Similarity Score: {result['similarity_score']:.4f}\n"
            f"Text: {result['text']}\n"
            f"Conversation ID: {result['conversation_id']}\n"
            f"Distance: {result['distance']:.4f}\n"
            f"{'-' * 80}\n\n"
        )
    
    if not search_results:
        output += "No results found.\n"
    
    print("Search and formatting completed.")
    return search_results, output