# -*- coding: utf-8 -*-
from lxml import etree
import requests


def get_xml():
    req_url = "https://express.tnt.com/expressconnect/shipping/ship"
    req_body = "xml_in=GET_LABEL:926734877"
    req_headers = {"Content-Type": "application/x-www-form-urlencoded"}
    label_response = requests.post(req_url, data=req_body, headers=req_headers)
    label_res_text = label_response.text.encode('utf-8')
    return etree.XML(label_res_text)


def get_xsl():
    req_url = "https://express.tnt.com/expresswebservices-website/stylesheets/HTMLAddressLabelRenderer.xsl"
    xsl_response = requests.get(req_url)
    xsl_response_text = xsl_response.text.encode('utf-8')
    return etree.XML(xsl_response_text)

xml = get_xml()
print xml.find(".//CONNUMBER").text
xslt = get_xsl()
transform = etree.XSLT(xslt)
dom = transform(xml)
# print et.tostring(dom, pretty_print=True)

for barcode_elem in dom.xpath("//td[@height='150']/img"):
    new_barcode = "<img src='https://express.tnt.com/barbecue/?data={barcode_number}&amp;type=UCC128&amp;appid=6&amp;height=105'/>".format(
        barcode_number=barcode_elem.getparent().text)
    barcode_elem.addnext(etree.XML(new_barcode))
    barcode_elem.getparent().remove(barcode_elem)

for pixel_elem in dom.xpath("//img[@width='1']"):
    pixel_elem.getparent().remove(pixel_elem)

# for pagebreak_elem in dom.xpath("//script")[1:]:
#     new_pagebreak = "<div style='page-break-after: always;'></div>"
#     pagebreak_elem.addnext(etree.XML(new_pagebreak))
#     pagebreak_elem.getparent().remove(pagebreak_elem)

for td_elem in dom.xpath("//td"):
    # print td_elem.text
    if td_elem.text and "\xc3\x82\xc2\xa0" in td_elem.text.encode("utf-8"):
        td_elem.text = td_elem.text.encode("utf-8").replace("\xc3\x82\xc2\xa0", "").decode("utf-8")

for td_elem in dom.xpath("//td[@class='tntTelephone']"):
    # import pdb;pdb.set_trace()
    td_elem.addnext(etree.XML("<td nowrap='nowrap' class='tntTelephone' align='center'>Telephone <br/> 01827 303030</td>"))
    td_elem.getparent().remove(td_elem)
    # print td_elem.text

# print etree.tostring(dom, pretty_print=True)

