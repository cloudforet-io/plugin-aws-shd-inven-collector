from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.service_health_dashboard.data import Event
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, DateTimeDyField, EnumDyField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta


service_meta = ItemDynamicLayout.set_fields('Event', fields=[
    TextDyField.data_source('Product Name', 'data.product_name'),
    TextDyField.data_source('Product', 'data.product'),
    TextDyField.data_source('Title', 'data.title'),
    EnumDyField.data_source('State', 'data.state', default_state={
        'safe': ['RESOLVED'],
        'alert': ['ERROR']
    }),
    TextDyField.data_source('Description', 'data.description'),
    TextDyField.data_source('Description (Translate)', 'data.translate.translated_text'),
    TextDyField.data_source('Region Name', 'data.region_name'),
    TextDyField.data_source('Region Code', 'region_code'),
    TextDyField.data_source('Translate Enabled', 'data.translate.translate_enable'),
    TextDyField.data_source('Translate Language', 'data.translate.translate_language'),
    DateTimeDyField.data_source('Publish Time', 'data.publish_date'),
])

metadata = CloudServiceMeta.set_layouts(layouts=[service_meta])


class ServiceHealthDashboardResource(CloudServiceResource):
    cloud_service_group = StringType(default='ServiceHealthDashboard')


class EventResource(ServiceHealthDashboardResource):
    cloud_service_type = StringType(default='Event')
    data = ModelType(Event)
    _metadata = ModelType(CloudServiceMeta, default=metadata, serialized_name='metadata')


class EventResponse(CloudServiceResponse):
    resource = PolyModelType(EventResource)
