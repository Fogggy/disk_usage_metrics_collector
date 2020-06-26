import logging
import shutil
from datetime import datetime

from elasticsearch_dsl import Document, Date, Long, Keyword
from elasticsearch_dsl.connections import connections

from settings import ELASTICSEARCH_HOST, ELASTICSEARCH_INDEX, ELASTICSEARCH_PASSWORD, ELASTICSEARCH_USERNAME, \
    MACHINE_NAME

logging.basicConfig(level=logging.INFO)


class MetricItem(Document):
    timestamp = Date()
    machine_name = Keyword()
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
    machine_name=MACHINE_NAME,
    total=total,
    used=used,
    free=free
)
metric.save()

logging.info(f"TOTAL: {total}, USED: {used}, FREE: {free}")
