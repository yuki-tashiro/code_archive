import fitz  # PyMuPDF
from markdownify import markdownify as md

"""
!pip install PyMuPDF
!pip install pymupdf4llm
!pip install markdown
!pip install markdownify
"""

def pdf_to_markdown(pdf_path, output_path):
    # PDFファイルを読み込む
    pdf_document = fitz.open(pdf_path)
    markdown_text = ""

    # 各ページを解析し、テキストを抽出してMarkdownに変換
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text = page.get_text("text")
        markdown_text += md(text)

    # Markdown形式のコンテンツをファイルに保存
    with open(output_path, "w") as md_file:
        md_file.write(markdown_text)

# PDFからMarkdownへの変換を実行
# pdf_path = "https://www.mhlw.go.jp/seisakunitsuite/bunya/kenkou_iryou/iryou/topics/dl/tp240424-01a_01.pdf"
pdf_path = "/content/drive/MyDrive/MatsuoLab/LLaVA-Med-JP/data/tp240424-01a_01.pdf"
output_path = "/content/drive/MyDrive/MatsuoLab/LLaVA-Med-JP/data/output.md"
pdf_to_markdown(pdf_path, output_path)