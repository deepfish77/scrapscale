from ftplib import FTP
import pysftp
import logging
import boto3

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FTPClient:
    def __init__(self):
        """
        Initialize FTPClient with credentials fetched from AWS SSM Parameter Store.
        """
        self.ssm = boto3.client("ssm")

        try:
            self.FTP_USER_LOGIN = self.ssm.get_parameter(
                Name="/your_ftp_path/", WithDecryption=True
            )["Parameter"]["Value"]

            self.FTP_USER_PASSWORD = self.ssm.get_parameter(
                Name="/your_ftp_path/password", WithDecryption=True
            )["Parameter"]["Value"]

            self.FTP_USER_NAME = self.ssm.get_parameter(
                Name="/your_ftp_path/username", WithDecryption=True
            )["Parameter"]["Value"]

            self.FTP_ENDPOINT = self.ssm.get_parameter(
                Name="/your_ftp_path/endpoint", WithDecryption=True
            )["Parameter"]["Value"]

            logger.info("Successfully fetched FTP credentials from SSM.")

        except Exception as e:
            logger.error(f"Failed to fetch FTP credentials from SSM: {e}")
            raise

    def connect_to_sftp_and_return_files(self, remote_path="Inbox"):
        """
        Connect to an SFTP server and list files in the specified remote directory.

        :param remote_path: The directory on the SFTP server to list files from.
        :return: A list of files in the specified remote directory.
        """
        logger.info("Connecting to SFTP...")
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None

        try:
            with pysftp.Connection(
                self.FTP_ENDPOINT,
                username=self.FTP_USER_NAME,
                password=self.FTP_USER_PASSWORD,
                port=22,
                cnopts=cnopts,
            ) as sftp:

                with sftp.cd(remote_path):
                    inbox = sftp.listdir(remotepath=".")
                    logger.info(f"SFTP Inbox files: {inbox}")
                    return inbox

        except Exception as e:
            logger.error(f"Failed to connect to SFTP or retrieve files: {e}")
            return []

    def connect_to_ftp_and_return_files(self, remote_path="Inbox"):
        """
        Connect to a standard FTP server and list files in the specified remote directory.

        :param remote_path: The directory on the FTP server to list files from.
        :return: A list of files in the specified remote directory.
        """
        logger.info("Connecting to FTP...")
        files = []

        try:
            with FTP(self.FTP_ENDPOINT) as ftp:
                ftp.login(user=self.FTP_USER_LOGIN, passwd=self.FTP_USER_PASSWORD)
                ftp.cwd(remote_path)
                ftp.retrlines("LIST", files.append)
                logger.info(f"FTP Inbox files: {files}")

        except Exception as e:
            logger.error(f"Failed to connect to FTP or retrieve files: {e}")
            return []

        return files
