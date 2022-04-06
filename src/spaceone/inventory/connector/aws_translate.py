import logging
from botocore.exceptions import ClientError

from spaceone.inventory.libs.connector import AWSConnector
from spaceone.inventory.error.custom import *

__all__ = ['AWSTranslateConnector']
_LOGGER = logging.getLogger(__name__)


class AWSTranslateConnector(AWSConnector):
    service = 'translate'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def translate(self, text, source_language_code, target_language_code):
        response = self.client.translate_text(Text=text,
                                              SourceLanguageCode=source_language_code,
                                              TargetLanguageCode=target_language_code)
        return response.get('TranslatedText')
