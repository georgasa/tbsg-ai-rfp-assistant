from docx import Document

doc = Document('final_verified_document.docx')
print('=== FINAL VERIFIED WORD DOCUMENT STRUCTURE ===')
print()
for i, para in enumerate(doc.paragraphs[:15]):
    if para.text.strip():
        if para.style.name.startswith('Heading'):
            print(f'HEADING {para.style.name}: {para.text}')
        elif para.style.name == 'List Bullet':
            # Show first 80 characters of bullet points
            content = para.text.strip()
            if len(content) > 80:
                content = content[:80] + '...'
            print(f'BULLET: {content}')
        else:
            # Show first 120 characters of regular paragraphs
            content = para.text.strip()
            if len(content) > 120:
                content = content[:120] + '...'
            print(f'PARAGRAPH {i}: {content}')
        print()

