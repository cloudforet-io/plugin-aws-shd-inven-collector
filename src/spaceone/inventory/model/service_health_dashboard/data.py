from schematics import Model
from schematics.types import StringType, DateTimeType, BooleanType, ModelType


class Translate(Model):
    translate_enable = BooleanType(serialize_when_none=False)
    translated_text = StringType(default='')
    translate_language = StringType(default='')


class Event(Model):
    guid = StringType()
    title = StringType(default='')
    description = StringType(default='')
    translate = ModelType(Translate)
    publish_date = DateTimeType(serialize_when_none=False)
    product = StringType(serialize_when_none=False)
    product_name = StringType(serialize_when_none=False)

    def reference(self):
        return {
            "resource_id": self.guid,
            "external_link": f"https://health.aws.amazon.com/health/status"
        }
