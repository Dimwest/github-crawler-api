import os
import json
from typing import Union
from functools import lru_cache
from botocore.exceptions import ClientError
from boto3 import session
from chalicelib.log import logger, with_logging


@with_logging
@lru_cache(maxsize=32)
def retrieve_secret(env_secret: Union[str, None] = None) -> dict:
    """ Connects to AWS Secrets Manager and obtains credentials. """
    secret = os.environ.get(env_secret, None)

    assert secret, "Name of the secret not found. Check ENV variable."

    try:
        logger.info(f"Retrieving the secret from AWS, secret name: {secret}")
        cs = session.Session()
        client = cs.client(service_name="secretsmanager")
        secret_value = client.get_secret_value(SecretId=secret)
    except ClientError as e:
        raise e
    else:
        logger.info(f"Retrieved the secret from AWS, secret name: {secret}")

        if "SecretBinary" in secret_value:
            return json.loads(secret_value["SecretBinary"])

        return json.loads(secret_value["SecretString"])
