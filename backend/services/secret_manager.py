import boto3
import json
import logging

import boto3.session

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def get_secret_by_arn(secret_arn, region_name="us-east-2"):
    """
    Retrieves a secret from AWS Secrets Manager using its ARN.

    Args:
        secret_arn (str): The ARN of the secret.
        region_name (str, optional): The AWS region. If None, the region is inferred from the environment. Defaults to None.

    Returns:
        dict or str: The secret value as a dictionary (if JSON) or a string.
        None: If an error occurs.
    """
    try:
        if region_name:
            session = boto3.session.Session(region_name=region_name)
            client = session.client(service_name="secretsmanager")
        else:
            client = boto3.client(service_name="secretsmanager")

        get_secret_value_response = client.get_secret_value(
            SecretId=secret_arn
        )  # Use SecretId with ARN
    except Exception as e:
        logger.error(f"Error retrieving secret with ARN '{secret_arn}': {e}")
        return None

    else:
        if "SecretString" in get_secret_value_response:
            secret = get_secret_value_response["SecretString"]
            try:
                secret_dict = json.loads(secret)
                return secret_dict
            except json.JSONDecodeError:
                return secret
        elif "SecretBinary" in get_secret_value_response:
            import base64

            binary_secret_data = base64.b64decode(
                get_secret_value_response["SecretBinary"]
            )
            return binary_secret_data.decode("utf-8")  # Or other appropriate decoding
        else:
            logger.warning(
                f"Secret with ARN '{secret_arn}' has no SecretString or SecretBinary."
            )
            return None
