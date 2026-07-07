from lxml import etree
from app.document_engine.rendering.docx.xml import qn


PICTURE_URI = "http://schemas.openxmlformats.org/drawingml/2006/picture"

EXT_BY_MIME = {
    "image/png": "png",
    "image/jpeg": "jpeg",
    "image/gif": "gif",
    "image/bmp": "bmp",
}

def build_image_run(
    rid: str,
    cx: int,
    cy: int,
    pic_id: int,
) -> etree._Element:
    
    run = etree.Element(qn("w:r"))
    drawing = etree.SubElement(run, qn("w:drawing"))

    inline = etree.SubElement(drawing, qn("wp:inline"))
    for a in ("distT", "distB", "distL", "distR"):
        inline.set(a, "0")

    ext = etree.SubElement(inline, qn("wp:extent"))
    ext.set("cx", str(cx))
    ext.set("cy", str(cy))

    doc_pr = etree.SubElement(inline, qn("wp:docPr"))
    doc_pr.set("id", str(pic_id))
    doc_pr.set("name", f"Picture {pic_id}")

    graphic = etree.SubElement(inline, qn("a:graphic"))
    gdata = etree.SubElement(graphic, qn("a:graphicData"))
    gdata.set("uri", PICTURE_URI)

    pic = etree.SubElement(gdata, qn("pic:pic"))

    nv = etree.SubElement(pic, qn("pic:nvPicPr"))
    cnv = etree.SubElement(nv, qn("pic:cNvPr"))
    cnv.set("id", str(pic_id))
    cnv.set("name", f"Picture {pic_id}")
    etree.SubElement(nv, qn("pic:cNvPicPr"))

    blip_fill = etree.SubElement(pic, qn("pic:blipFill"))
    etree.SubElement(blip_fill, qn("a:blip")).set(qn("r:embed"), rid)
    stretch = etree.SubElement(blip_fill, qn("a:stretch"))
    etree.SubElement(stretch, qn("a:fillRect"))

    sp_pr = etree.SubElement(pic, qn("pic:spPr"))
    xfrm = etree.SubElement(sp_pr, qn("a:xfrlm"))
    off = etree.SubElement(xfrm, qn("a:off"))
    off.set("x", "0")
    off.set("y", "0")
    a_ext = etree.SubElement(xfrm, qn("a:ext"))
    a_ext.set("cx", str(cx))
    a_ext.set("cy", str(cy))
    geom = etree.SubElement(sp_pr, qn("a:prstGeom"))
    geom.set("prst", "rect")
    etree.SubElement(geom, qn("a:avLst"))

    return run