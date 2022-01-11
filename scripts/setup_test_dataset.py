"""Extract places dataset, used in the tests"""
import re
import os
import multiprocessing
import xml
from typing import List

import requests
from loguru import logger
from rdflib import Graph

BASE_URL = 'https://ontologi.es/place/'
DATASET_DIR = "dataset"
WORKERS = multiprocessing.cpu_count() * 2 + 1


def setup_dir():
    """Create dataset folder"""
    logger.info("Setting up dataset dir.")
    if os.path.isdir(DATASET_DIR):
        logger.error(f"Dataset dir already exists: {DATASET_DIR}")
        exit(1)

    os.mkdir(DATASET_DIR)


def data_file_path(filename: str) -> str:
    return os.path.join(DATASET_DIR, filename)


def save_file(filename: str, content: str):
    with open(data_file_path(filename), 'w') as fp:
        fp.write(content)


def download_base_url() -> List[str]:
    """Download base URL and return list of other URLs"""
    logger.info(f'Downloading the base URL: {BASE_URL}')

    text = requests.get(BASE_URL).text
    save_file('base.rdf', text)

    urls = re.findall(r'(?<=rdf:about=").+(?=" s)', text)
    return urls


def download_url(url: str):
    logger.info(f"Downloading {url}")
    filename = url.split('/')[-1] + '.rdf'

    try:
        r = requests.get(url)
        if r.status_code != 200:
            logger.error(
                f"Failed to fetch {url}: status_codes={r.status_code}")
            return
        text = r.text

    except Exception as e:
        logger.error(f"Failed to fetch {url}: {e}")
        return

    save_file(filename, text)


def fuse_dataset(filename: str):
    files = [os.path.join(DATASET_DIR, file)
             for file in os.listdir(DATASET_DIR)]
    graph = Graph()
    for file in files:
        try:
            graph.parse(file)
        except xml.sax.SAXParseException:
            logger.error(f"Failed to parse: {file}")
            logger.info("Skiping...")

    graph.serialize(data_file_path(filename),
                    format="application/rdf+xml")


if __name__ == '__main__':
    setup_dir()
    urls = download_base_url()

    with multiprocessing.Pool(WORKERS) as p:
        p.map(download_url, urls)

    logger.info("Fusing dataset")

    fuse_dataset('dataset.rdf')
