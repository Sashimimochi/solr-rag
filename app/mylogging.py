import logging

formatter = '='*50 + '\n[%(levelname)s] : %(asctime)s : %(message)s'
logging.basicConfig(level=logging.INFO, format=formatter)
logger = logging.getLogger(__name__)
