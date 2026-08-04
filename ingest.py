import os
import re
import fitz  # PyMuPDF
import uuid
import chromadb
from chromadb.utils import embedding_functions

class Ingestor:
    def __init__(self, db_path="./data/chroma_aviation"):
        self.db_path = os.path.abspath(db_path)
        self.client = chromadb.PersistentClient(path=self.db_path)
        self.collection = self.client.get_or_create_collection(
            name="knowledge",
            embedding_function=embedding_functions.DefaultEmbeddingFunction()
        )

    def extract_metadata(self, doc, file_path):
        meta = doc.metadata or {}
        author = meta.get("author") or "Unknown Author"
        year = "2026"
        creation_date = meta.get("creationDate")
        if creation_date:
            match = re.search(r'\d{4}', creation_date)
            if match:
                year = match.group(0)
        return author, year

    def parse_sections_and_math(self, file_path):
        doc = fitz.open(file_path)
        author, year = self.extract_metadata(doc, file_path)
        
        current_section = "General"
        sections_data = {"General": []}
        target_sections = ["Fuselage", "Hydraulics", "Propulsion", "Avionics"]
        for sec in target_sections:
            sections_data[sec] = []
            
        math_formulas = []
        block_math_pat = re.compile(r'\$\$(.*?)\$\$', re.DOTALL)
        inline_math_pat = re.compile(r'\$([^\$]+?)\$')

        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            
            # Find block math
            blocks = block_math_pat.findall(text)
            for block in blocks:
                math_formulas.append((block.strip(), page_num, "block"))
                
            # Find inline math
            inlines = inline_math_pat.findall(text)
            for inline in inlines:
                if any(c in inline for c in ['=', '+', '-', '*', '/', '\\', '^', '_']):
                    math_formulas.append((inline.strip(), page_num, "inline"))

            lines = text.split("\n")
            for line in lines:
                line_clean = line.strip()
                if not line_clean:
                    continue
                
                # Check for section triggers
                for sec in target_sections:
                    if sec.lower() in line_clean.lower():
                        current_section = sec
                        break
                
                if current_section in sections_data:
                    sections_data[current_section].append(line_clean)
                    
        processed_sections = {k: " ".join(v) for k, v in sections_data.items() if v}
        return author, year, processed_sections, math_formulas

    def ingest_pdf(self, pdf_path):
        try:
            author, year, sections, math_formulas = self.parse_sections_and_math(pdf_path)
            source_filename = os.path.basename(pdf_path)
            
            # Index text sections
            for section_name, text in sections.items():
                if not text.strip():
                    continue
                chunks = [text[i:i+1500] for i in range(0, len(text), 1200)]
                for idx, chunk in enumerate(chunks):
                    self.collection.add(
                        documents=[chunk],
                        metadatas=[{
                            "source": source_filename,
                            "type": "text",
                            "section": section_name,
                            "author": author,
                            "year": year,
                            "chunk_index": idx
                        }],
                        ids=[f"text_{uuid.uuid()}"]
                    )
            
            # Index formulas
            for idx, (formula, page_num, f_type) in enumerate(math_formulas):
                description = f"LaTeX mathematical formula ({f_type}): {formula}"
                self.collection.add(
                    documents=[description],
                    metadatas=[{
                        "source": source_filename,
                        "type": "math",
                        "page": page_num,
                        "author": author,
                        "year": year,
                        "formula_type": f_type,
                        "raw_latex": formula
                    }],
                    ids=[f"math_{uuid.uuid()}"]
                )
                
            return {"success": True, "formulas_count": len(math_formulas)}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def ingest_directory(self, directory_path):
        os.makedirs(directory_path, exist_ok=True)
        files = os.listdir(directory_path)
        results = []
        for file in files:
            if file.lower().endswith(".pdf"):
                file_path = os.path.join(directory_path, file)
                res = self.ingest_pdf(file_path)
                results.append((file, res))
        return results
