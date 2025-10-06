from docx import Document
from word_generator import WordDocumentGenerator

# Create a test combined_analysis
combined_analysis = {
    'pillar': 'Integration',
    'products': ['Transact'],
    'region': 'GLOBAL',
    'total_api_calls': 2,
    'product_analyses': [
        {
            'product': 'Transact',
            'analysis': {
                'answers': [
                    'First answer - key points',
                    'Second answer - detailed analysis'
                ]
            }
        }
    ]
}

# Create document generator
gen = WordDocumentGenerator()

# Create document
doc_path = gen.create_combined_document(combined_analysis)

if doc_path:
    print(f"Document created: {doc_path}")
    
    # Now check the document structure
    doc = Document(doc_path)
    print("\n=== Document Structure ===")
    for i, para in enumerate(doc.paragraphs[:10]):
        if para.text.strip():
            print(f"Paragraph {i}: Style={para.style.name}, Text=\"{para.text[:50]}...\"")
else:
    print("Document creation failed")

