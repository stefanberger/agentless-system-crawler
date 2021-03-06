import logging

import utils.dockerutils
from icrawl_plugin import IContainerCrawler
from utils.connection_utils import crawl_connections
from utils.namespace import run_as_another_namespace, ALL_NAMESPACES

logger = logging.getLogger('crawlutils')


class ConnectionContainerCrawler(IContainerCrawler):

    def get_feature(self):
        return 'connection'

    def crawl(self, container_id, avoid_setns=False, **kwargs):
        inspect = utils.dockerutils.exec_dockerinspect(container_id)
        state = inspect['State']
        pid = str(state['Pid'])
        logger.debug(
            'Crawling %s for container %s' %
            (self.get_feature(), container_id))

        if avoid_setns:
            raise NotImplementedError('avoidsetns mode not implemented')
        else:  # in all other cases, including wrong mode set
            return run_as_another_namespace(pid,
                                            ALL_NAMESPACES,
                                            crawl_connections)
