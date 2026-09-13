from pypdf import PdfReader #we'll use to extract text from the uploaded PDF
import csv

#pdf reader
def extract_pdf_text(source):
    reader = PdfReader(source)

    pages = []

    for page in reader.pages:  #Go through every page of the PDF
        text = page.extract_text() or ""
        pages.append(text)

    return "\n\n".join(pages)  #Combine all pages into one large text string



# txt reader
def extract_txt_text(source):
    text = source.read()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    return text


#csv reader
def extract_csv_text(source):
    text = source.read().decode("utf-8")

    rows = csv.reader(text.splitlines())

    lines = []

    for row in rows:
        lines.append(" | ".join(row))

    return "\n".join(lines)


#general function to reads files
def extract_text(source, filename):
    if filename.lower().endswith(".pdf"):
        return extract_pdf_text(source)

    elif filename.lower().endswith(".txt"):
        return extract_txt_text(source)

    elif filename.lower().endswith(".csv"):
        return extract_csv_text(source)

    else:
        raise ValueError("Unsupported file type")