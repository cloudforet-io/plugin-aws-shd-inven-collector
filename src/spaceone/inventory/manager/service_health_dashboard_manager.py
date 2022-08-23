import time
import logging
import json
import re
import ssl
from datetime import datetime
from pytz import timezone
from urllib.request import urlopen
import xml.etree.ElementTree as ET

from spaceone.inventory.libs.manager import AWSManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.libs.schema.error_resource import ErrorResourceResponse
from spaceone.inventory.connector.aws_translate import AWSTranslateConnector
from spaceone.inventory.conf.cloud_service_conf import *
from spaceone.inventory.model.service_health_dashboard.data import Event, Translate
from spaceone.inventory.model.service_health_dashboard.cloud_service import EventResource, EventResponse
from spaceone.inventory.model.service_health_dashboard.cloud_service_type import CLOUD_SERVICE_TYPES

_LOGGER = logging.getLogger(__name__)


class ServiceHealthDashboardManager(AWSManager):
    connector_name = 'AWSTranslateConnector'
    cloud_service_group = 'ServiceHealthDashboard'
    cloud_service_type = 'Service'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_services(self, params):
        _LOGGER.debug("** Service Health Dashboard Start **")
        options = params.get('options', {})

        start_time = time.time()
        event_resources = []

        tree = self.get_element_tree_from_url(SHD_FEED_URL)

        if tree.findall('channel/item'):
            for element in tree.findall('channel/item'):
                try:
                    guid = element.findtext('guid', '')
                    description = element.findtext('description', '')

                    resource = {
                        'title': self.refine_title(element.findtext('title', '')),
                        'state': self.get_state_from_title(element.findtext('title', '')),
                        'guid': guid,
                        'description': description,
                    }

                    if publish_date := self.convert_datetime_utc(element.findtext('pubDate', '')):
                        resource.update({'publish_date': publish_date})

                    product, region = self.get_product_region_from_guid(guid)

                    resource.update({
                        'product': product,
                        'product_name': PRODUCT_MAP.get(product, product)
                    })

                    if translate_enable := options.get('translate_enable', True):
                        try:
                            translate = Translate({
                                'translate_enable': translate_enable,
                                'translated_text': self.translate_description(description, params),
                                'translate_language': options.get('target_lang_code', TARGET_LANG_CODE)
                            }, strict=False)

                            resource.update({'translate': translate})
                            # Avoid an errors due to too fast API calls
                            time.sleep(0.3)
                        except Exception as e:
                            error_resource_response = self.generate_error(guid, '', e)
                            event_resources.append(error_resource_response)

                    service_data = Event(resource, strict=False)
                    service_resource = EventResource({
                        'name': service_data.title,
                        'data': service_data,
                        'region_code': region,
                        'reference': ReferenceModel(service_data.reference())
                    })
                    event_resources.append(EventResponse({'resource': service_resource}))

                except Exception as e:
                    resource_arn = element.findtext('guid', '')
                    error_resource_response = self.generate_error(resource_arn, '', e)
                    event_resources.append(error_resource_response)

        _LOGGER.debug(f' Service Health Dashboard Finished {time.time() - start_time} Seconds')
        return event_resources

    def translate_description(self, description, params):
        translate_conn: AWSTranslateConnector = self.locator.get_connector(self.connector_name, **params)
        translate_conn.set_client()
        translate_options = params.get('options', {}).get('translate_options', {})

        return translate_conn.translate(description,
                                        translate_options.get('source_lang_code', SOURCE_LANG_CODE),
                                        translate_options.get('target_lang_code', TARGET_LANG_CODE))

    def generate_error(self, resource_arn, service, error_message):
        _LOGGER.error(f'[generate_error] [{service}] {error_message}')

        if isinstance(error_message, dict):
            error_resource_response = ErrorResourceResponse(
                {'message': json.dumps(error_message),
                 'resource': {'resource_id': resource_arn,
                              'cloud_service_group': self.cloud_service_group,
                              'cloud_service_type': self.cloud_service_type}})

        else:
            error_resource_response = ErrorResourceResponse(
                {'message': str(error_message),
                 'resource': {'resource_id': resource_arn,
                              'cloud_service_group': self.cloud_service_group,
                              'cloud_service_type': self.cloud_service_type}})

        return error_resource_response

    @staticmethod
    def get_product_region_from_guid(guid):
        # pattern match using re if guid type is 'http://status.aws.amazon.com/#ec2-ap-northeast-1_1587391740'
        if re.match(r"^http:\/\/status.aws.amazon.com\/\#(.*)-(ap|us|ca|eu|me|sa)-([a-z]*)-(\d{1})_(.*)", guid):
            match = re.search(
                '^http:\/\/status.aws.amazon.com\/\#(.*)-(ap|us|ca|eu|me|sa)-([a-z]*)-(\d{1})_(.*)', guid)
            product = match.group(1)
            region = match.group(2) + "-" + match.group(3) + "-" + match.group(4)
        # pattern match using re if guid type is 'http://status.aws.amazon.com/#cloudfront_1499437860'
        elif re.match(r"^http:\/\/status.aws.amazon.com\/\#(.*)_(.*)", guid):
            match = re.search('^http:\/\/status.aws.amazon.com\/\#(.*)_(.*)', guid)
            product = match.group(1)  # value
            region = "global"  # value
        else:
            product = "Service"
            region = "Unknown"

        return product, region

    @staticmethod
    def get_element_tree_from_url(url):
        context = ssl._create_unverified_context()
        feed_url = urlopen(url, context=context)
        return ET.parse(feed_url)

    @staticmethod
    def convert_datetime_utc(publish_date):
        tz = ''
        try:
            if "PDT" in publish_date:
                tz = 'PDT'
            elif "PST" in publish_date:
                tz = 'PST'

            dtobj = datetime.strptime(publish_date, f'%a, %d %b %Y %H:%M:%S {tz}')
            return dtobj.replace(tzinfo=timezone('UTC'))
        except Exception as e:
            return None

    @staticmethod
    def refine_title(title):
        title = title.replace('Informational message: ', '')
        title = title.replace('Service is operating normally: ', '')

        return title

    @staticmethod
    def get_state_from_title(title):
        state = 'ERROR'

        if 'RESOLVED' in title:
            state = 'RESOLVED'

        return state
