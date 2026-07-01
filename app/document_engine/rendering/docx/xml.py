from app.document_engine.parser.namespaces import NS

XML_NS = "http://www.w3.org/XML/1998/namespace"

WORD_NSMAP = {k: NS[k] for k in ("w", "r", "wp", "a", "pic")}

def qn(tag: str) -> str:
    """Clark notation for lxml: 'w:p' -> '{http://...wordprocessingml...}p' """

    prefix, local = tag.split(":")
    return f"{{{NS[prefix]}}}{local}"