import email
import email.header
from datetime import datetime
import re
from bs4 import BeautifulSoup


def replace_characters(text):
    try:
        # Tentar decodificar a string
        decoded_text = email.header.decode_header(text)
        decoded_text = [part[0].decode(part[1] or 'utf-8') for part in decoded_text if part[0] is not None]
        return ' '.join(decoded_text)
    except:
        # Se não for possível decodificar, apenas remover caracteres especiais
        modified_text = text.replace("<", " - ").replace(">", "")
        modified_text = modified_text.replace("\"", " ")
        modified_text = modified_text.strip()
        return modified_text


def decode_subject(encoded_subject):
    decoded_subject = email.header.decode_header(encoded_subject)
    decoded_subject_str = ""
    for part in decoded_subject:
        if isinstance(part[0], bytes):
            decoded_subject_str += part[0].decode(part[1] or 'utf-8')
        else:
            decoded_subject_str += part[0]
    return decoded_subject_str

def formatDate(date):
    return datetime(2024, 5, 21).strftime('%d/%m/%Y')


def decode_body(message):
    def get_charset(part):
        charset = part.get_content_charset()
        if charset is None:
            charset = 'utf-8'
        return charset

    def decode_part(part):
        charset = get_charset(part)
        payload = part.get_payload(decode=True)
        if payload:
            return payload.decode(charset, errors='replace')
        return ''

    def clean_html(html):
        soup = BeautifulSoup(html, 'html.parser')

        # Remove script and style elements
        for script_or_style in soup(['script', 'style']):
            script_or_style.decompose()

        # Remove anchor tags but keep the text inside
        for anchor in soup.find_all('a'):
            anchor.replace_with(anchor.get_text())

        # Remove img tags but keep the alt text if available
        for img in soup.find_all('img'):
            alt_text = img.get('alt', '')
            img.replace_with(alt_text)

        # Remove all other tags except for a basic set
        for tag in soup.find_all(True):
            if tag.name not in ['p', 'br', 'strong', 'em', 'b', 'i', 'u']:
                tag.unwrap()

        # Get text and remove extra whitespace
        text = soup.get_text(separator=' ')
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    if message.is_multipart():
        text_parts = []
        html_parts = []
        
        for part in message.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            if "attachment" not in content_disposition:
                if content_type == "text/plain":
                    text_parts.append(decode_part(part))
                elif content_type == "text/html":
                    html_parts.append(decode_part(part))

        # Prefer text/plain over text/html
        if text_parts:
            return '\n'.join(text_parts)
        elif html_parts:
            html_content = '\n'.join(html_parts)
            return clean_html(html_content)
    else:
        content_type = message.get_content_type()
        if content_type == "text/plain":
            return decode_part(message)
        elif content_type == "text/html":
            html_content = decode_part(message)
            return clean_html(html_content)

    return ""