import xml.etree.ElementTree as ET
from typing import Dict

class XMLProcessor:

    def parse_credit_limit_rq(self, xml_content: str) -> Dict:
        try:
            root = ET.fromstring(xml_content)

            request_data = {
                'CodeClientBackOffice': self._get_element_text(root, 'CodeClientBackOffice'),
                'CodeClientOBT': self._get_element_text(root, 'CodeClientOBT'),
                'Name': self._get_element_text(root, 'Name'),
                'locValidacion': self._get_element_text(root, 'locValidacion'),
                'value': float(self._get_element_text(root, 'value', '0')),
                'Currency': self._get_element_text(root, 'Currency'),
                'product': self._get_element_text(root, 'product'),
                'description': self._get_element_text(root, 'description'),
                'paymentType': self._get_element_text(root, 'paymentType'),
                'mailUser': self._get_element_text(root, 'mailUser')
            }

            return request_data

        except Exception as e:
            raise ValueError(f"Error parsing XML request: {str(e)}")

    def generate_credit_limit_rs(
        self,
        code_client_backoffice: str,
        code_client_obt: str,
        status: str,
        message: str
    ) -> str:
        root = ET.Element('CreditLimitRS')

        code_backoffice_elem = ET.SubElement(root, 'CodeClientBackOffice')
        code_backoffice_elem.text = str(code_client_backoffice)

        code_obt_elem = ET.SubElement(root, 'CodeClientOBT')
        code_obt_elem.text = str(code_client_obt)

        status_elem = ET.SubElement(root, 'status')
        status_elem.text = status

        message_elem = ET.SubElement(root, 'Message')
        message_elem.text = message

        xml_string = ET.tostring(root, encoding='unicode', method='xml')

        return f'<?xml version="1.0" encoding="UTF-8"?>\n{xml_string}'

    def _get_element_text(self, root: ET.Element, tag: str, default: str = '') -> str:
        element = root.find(tag)
        return element.text.strip() if element is not None and element.text else default
