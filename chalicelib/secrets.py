import os
import json
from typing import Union
from chalicelib.log import logger, with_logging
from functools import lru_cache
from boto3 import session
from botocore.exceptions import ClientError


@with_logging
@lru_cache(maxsize=32)
def retrieve_secret(env_secret: Union[str, None] = None) -> dict:
    """ Connects to AWS Secrets Manager and obtains credentials. """

    secret_name = os.environ.get(env_secret, None)
    assert secret_name, "Name of the secret not found. Check ENV variable."

    try:
        logger.info(f"Retrieving the secret from AWS, secret name: {secret_name}")
        cs = session.Session()
        client = cs.client(service_name="secretsmanager")
        secret_value = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        raise e
    else:
        logger.info(f"Retrieved the secret from AWS, secret name: {secret_name}")

        if "SecretBinary" in secret_value:
            return json.loads(secret_value["SecretBinary"])

        return json.loads(secret_value["SecretString"])
