#!/usr/bin/env python
import sys
import pathlib
from time import gmtime, strftime
import logging
import re
import json
import yaml
import getopt
import asyncio
from aiohttp import ClientSession
import aiofiles

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)
logger = logging.getLogger("areq")
logging.getLogger("chardet.charsetprober").disabled = True


# Create Test Data START
def parse_json_to_dict(path):
    with open(path) as file:
        raw_config = json.load(file)
        return raw_config


def extract_did_method(did):
    return re.findall("(?<=:)(.*?)(?=:)", did)[0]


def create_test_data(drivers_config, host):
    test_data = []
    for driver in drivers_config:
        did: str = driver["testIdentifiers"][0]
        if did.startswith("did:"):
            driver_test_data = {
                "method": extract_did_method(driver["testIdentifiers"][0]),
                "url": host + driver["testIdentifiers"][0]
            }
            test_data.append(driver_test_data)

    return test_data


# Create Test Data END

# Run tests START
async def fetch_html(url: str, session: ClientSession) -> str:
    resp = await session.request(method="GET", url=url)
    logger.info("Got response [%s] for URL: %s", resp.status, url)
    if resp.status != 200:
        html = await resp.text()
        print(html)
        return html
    else:
        return "Success"


async def parse(url, session):
    result = await fetch_html(url=url, session=session)
    return result


async def write_one(file, data, session):
    res = await parse(url=data['url'], session=session)
    if not res:
        return None
    async with aiofiles.open(file, "a") as f:
        await f.write(f"{data['url']}\t{res}\n")
        logger.info("Wrote results for source URL: %s", data['url'])


async def run_tests(file, test_data):
    async with ClientSession() as session:
        tasks = []
        for data in test_data:
            tasks.append(
                write_one(file=file, data=data, session=session)
            )
        await asyncio.gather(*tasks)


# Run tests END

def main(argv):
    ingress = '../out/uni-resolver-ingress.yaml'
    config = './test-config.json'
    try:
        opts, args = getopt.getopt(argv, "hi:c:", ["ingress=", "config="])
    except getopt.GetoptError:
        print('./smoke-test.py -i <ingress-file> -c <uni-resolver-config>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('./smoke-test.py -i <ingress-file> -c <uni-resolver-config>')
            sys.exit()
        elif opt in ("-i", "--ingress"):
            ingress = arg
        elif opt in ("-c", "--config"):
            config = arg

    # read config
    with open(ingress) as stream:
        ingress = yaml.safe_load(stream)
        host = ingress['spec']['rules'][0]['host']
        uni_resolver_path = "http://" + host + "/1.0/identifiers/"

    # build test data
    config_dict = parse_json_to_dict(config)
    test_data = create_test_data(config_dict["drivers"], uni_resolver_path)

    # run tests
    here = pathlib.Path(__file__).parent
    timestr = strftime("%d-%m-%Y_%H-%M-%S-UTC", gmtime())
    filename = "result-" + timestr + ".json"
    out_path = here.joinpath(filename)

    asyncio.run(run_tests(file=out_path, test_data=test_data))


if __name__ == "__main__":
    main(sys.argv[1:])
    print('Script finished')
