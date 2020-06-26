import logging
import shutil
from datetime import datetime

from elasticsearch_dsl import Document, Date, Long
from elasticsearch_dsl.connections import connections

from settings import ELASTICSEARCH_HOST, ELASTICSEARCH_INDEX, ELASTICSEARCH_PASSWORD, ELASTICSEARCH_USERNAME

logging.basicConfig(level=logging.INFO)


class MetricItem(Document):
    timestamp = Date()
    total = Long()
    used = Long()
    free = Long()

    class Index:
        name = ELASTICSEARCH_INDEX


# Define a default Elasticsearch client
connections.create_connection(hosts=[ELASTICSEARCH_HOST], http_auth=(ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD))

MetricItem.init()

total, used, free = shutil.disk_usage("/")
metric = MetricItem(
    timestamp=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
    total=total,
    used=used,
    free=free
)
metric.save()

logging.info(f"TOTAL: {total}, USED: {used}, FREE: {free}")
