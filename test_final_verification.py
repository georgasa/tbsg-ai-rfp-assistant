from word_generator import WordDocumentGenerator
import json

# Load the latest analysis
with open('latest_final_analysis.json', 'r') as f:
    analysis_data = json.load(f)

# Create document generator
gen = WordDocumentGenerator()

# Create Word document using create_combined_document
doc_path = gen.create_combined_document(analysis_data)

if doc_path:
    print(f"Document created: {doc_path}")
    
    # Check the document structure
    from docx import Document
    doc = Document(doc_path)
    print("\n=== FINAL VERIFICATION DOCUMENT STRUCTURE ===")
    for i, para in enumerate(doc.paragraphs[:25]):
        if para.text.strip():
            if para.style.name.startswith('Heading'):
                print(f'HEADING {para.style.name}: {para.text}')
            elif para.style.name == 'List Bullet':
                content = para.text.strip()
                if len(content) > 100:
                    content = content[:100] + '...'
                print(f'BULLET: {content}')
            else:
                content = para.text.strip()
                if len(content) > 120:
                    content = content[:120] + '...'
                print(f'PARAGRAPH {i}: {content}')
            print()
else:
    print("Document creation failed")
