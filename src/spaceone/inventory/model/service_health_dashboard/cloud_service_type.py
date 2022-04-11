from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, DateTimeDyField, EnumDyField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta


cst_shd = CloudServiceTypeResource()
cst_shd.name = 'Event'
cst_shd.provider = 'aws'
cst_shd.group = 'ServiceHealthDashboard'
cst_shd.labels = ['Management']
cst_shd.is_primary = True
cst_shd.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/aws.svg',
}

cst_shd._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Product Name', 'data.product_name'),
        TextDyField.data_source('Title', 'data.title'),
        EnumDyField.data_source('State', 'data.state', default_state={
            'safe': ['RESOLVED'],
            'alert': ['ERROR']
        }),
        DateTimeDyField.data_source('Publish Time', 'data.publish_date'),
    ],
    search=[
        SearchField.set(name='GUID', key='data.guid'),
        SearchField.set(name='Title', key='data.title'),
        SearchField.set(name='State', key='data.state'),
        SearchField.set(name='Region Code', key='data.region_code'),
        SearchField.set(name='Region Name', key='data.region_name'),
        SearchField.set(name='Product', key='data.product'),
        SearchField.set(name='Product Name', key='data.product_name'),
        SearchField.set(name='Description', key='data.description'),
        SearchField.set(name='Publish Date', key='data.publish_date', data_type='datetime'),
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_shd}),
]
