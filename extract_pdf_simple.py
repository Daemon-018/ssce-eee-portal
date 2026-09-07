from pypdf import PdfReader

pdf_path = '/data/data/com.termux/files/home/eee_site/r23_eee_syllabus.pdf'
try:
    reader = PdfReader(pdf_path)
    full_text = ''
    for page in reader.pages:
        full_text += page.extract_text() + '\n'
    
    with open('/data/data/com.termux/files/home/eee_site/syllabus_raw.txt', 'w', encoding='utf-8') as f:
        f.write(full_text)
    print('SUCCESS: Text dumped to syllabus_raw.txt')
except Exception as e:
    print(f'ERROR: {str(e)}')
