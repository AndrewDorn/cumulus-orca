"""
Name: test_copy_files_to_archive.py

Description:  Unit tests for copy_files_to_archive.py.
"""
import os
import unittest
import uuid
from random import randint
from unittest import mock
from unittest.mock import Mock, call, patch, MagicMock

from botocore.exceptions import ClientError

import copy_files_to_archive


class TestCopyFiles(unittest.TestCase):  # pylint: disable-msg=too-many-instance-attributes
    """
    TestCopyFiles.
    """

    @patch.dict(os.environ,
                {"COPY_RETRIES": '703', "COPY_RETRY_SLEEP_SECS": '108.5', 'DB_QUEUE_URL': 'something.blah'}, clear=True)
    @patch('copy_files_to_archive.task')
    def test_handler_happy_path(self,
                                mock_task: MagicMock):
        records = Mock()
        event = {'Records': records}

        result = copy_files_to_archive.handler(event, Mock())

        mock_task.assert_called_with(records, 703, 108.5, 'something.blah')
        self.assertEqual(mock_task.return_value, result)

    @patch.dict(os.environ, {'DB_QUEUE_URL': 'something.else'}, clear=True)
    @patch('copy_files_to_archive.task')
    def test_handler_uses_default_retry_settings(self,
                                                 mock_task: MagicMock):
        """
        If retry settings not in os.environ, uses 2 retries and 30 seconds.
        """
        records = Mock()
        event = {'Records': records}

        result = copy_files_to_archive.handler(event, Mock())

        mock_task.assert_called_with(records, 2, 30, 'something.else')
        self.assertEqual(mock_task.return_value, result)

    @patch('time.sleep')
    @patch('copy_files_to_archive.post_status_for_file_to_queue')
    @patch('copy_files_to_archive.copy_object')
    @patch('copy_files_to_archive.get_files_from_records')
    @patch('boto3.client')
    def test_task_happy_path(self,
                             mock_boto3_client: MagicMock,
                             mock_get_files_from_records: MagicMock,
                             mock_copy_object: MagicMock,
                             mock_post_status_for_file_to_queue: MagicMock,
                             mock_sleep: MagicMock):
        """
        If all files go through without errors, return without sleeps.
        """
        db_queue_url = uuid.uuid4().__str__()
        max_retries = randint(2, 9999)
        retry_sleep_secs = randint(0, 9999)

        file0_job_id = uuid.uuid4().__str__()
        file0_granule_id = uuid.uuid4().__str__()
        file0_input_filename = uuid.uuid4().__str__()
        file0_source_bucket = uuid.uuid4().__str__()
        file0_source_key = uuid.uuid4().__str__()
        file0_target_bucket = uuid.uuid4().__str__()
        file0_target_key = uuid.uuid4().__str__()

        file1_job_id = uuid.uuid4().__str__()
        file1_granule_id = uuid.uuid4().__str__()
        file1_input_filename = uuid.uuid4().__str__()
        file1_source_bucket = uuid.uuid4().__str__()
        file1_source_key = uuid.uuid4().__str__()
        file1_target_bucket = uuid.uuid4().__str__()
        file1_target_key = uuid.uuid4().__str__()

        mock_records = Mock()

        file0 = {
            copy_files_to_archive.INPUT_JOB_ID_KEY: file0_job_id,
            copy_files_to_archive.INPUT_GRANULE_ID_KEY: file0_granule_id,
            copy_files_to_archive.INPUT_FILENAME_KEY: file0_input_filename,
            copy_files_to_archive.FILE_SUCCESS_KEY: False,
            copy_files_to_archive.INPUT_SOURCE_BUCKET_KEY: file0_source_bucket,
            copy_files_to_archive.INPUT_SOURCE_KEY_KEY: file0_source_key,
            copy_files_to_archive.INPUT_TARGET_BUCKET_KEY: file0_target_bucket,
            copy_files_to_archive.INPUT_TARGET_KEY_KEY: file0_target_key
        }
        file1 = {
            copy_files_to_archive.INPUT_JOB_ID_KEY: file1_job_id,
            copy_files_to_archive.INPUT_GRANULE_ID_KEY: file1_granule_id,
            copy_files_to_archive.INPUT_FILENAME_KEY: file1_input_filename,
            copy_files_to_archive.FILE_SUCCESS_KEY: False,
            copy_files_to_archive.INPUT_SOURCE_BUCKET_KEY: file1_source_bucket,
            copy_files_to_archive.INPUT_SOURCE_KEY_KEY: file1_source_key,
            copy_files_to_archive.INPUT_TARGET_BUCKET_KEY: file1_target_bucket,
            copy_files_to_archive.INPUT_TARGET_KEY_KEY: file1_target_key
        }
        mock_get_files_from_records.return_value = [file0, file1]
        mock_copy_object.return_value = None

        copy_files_to_archive.task(mock_records, max_retries, retry_sleep_secs, db_queue_url)

        mock_get_files_from_records.assert_called_once_with(mock_records)
        mock_boto3_client.assert_called_once_with('s3')
        mock_copy_object.assert_has_calls([
            call(mock_boto3_client.return_value, file0_source_bucket, file0_source_key, file0_target_bucket,
                 file0_target_key),
            call(mock_boto3_client.return_value, file1_source_bucket, file1_source_key, file1_target_bucket,
                 file1_target_key)])
        self.assertEqual(2, mock_copy_object.call_count)
        mock_post_status_for_file_to_queue.assert_has_calls([
            call(file0_job_id, file0_granule_id, file0_input_filename, None, None,
                 copy_files_to_archive.ORCA_STATUS_SUCCESS, None, None,
                 mock.ANY, mock.ANY,
                 copy_files_to_archive.RequestMethod.PUT, db_queue_url, max_retries, retry_sleep_secs),
            call(file1_job_id, file1_granule_id, file1_input_filename, None, None,
                 copy_files_to_archive.ORCA_STATUS_SUCCESS, None, None,
                 mock.ANY, mock.ANY,
                 copy_files_to_archive.RequestMethod.PUT, db_queue_url, max_retries, retry_sleep_secs)])
        self.assertEqual(2, mock_post_status_for_file_to_queue.call_count)
        mock_sleep.assert_not_called()

    @patch('time.sleep')
    @patch('copy_files_to_archive.post_status_for_file_to_queue')
    @patch('copy_files_to_archive.copy_object')
    @patch('copy_files_to_archive.get_files_from_records')
    @patch('boto3.client')
    def test_task_retries_failed_files_up_to_retry_limit(self,
                                                         mock_boto3_client: MagicMock,
                                                         mock_get_files_from_records: MagicMock,
                                                         mock_copy_object: MagicMock,
                                                         mock_post_status_for_file_to_queue: MagicMock,
                                                         mock_sleep: MagicMock):
        """
        If one file causes errors during copy, retry up to limit then post error status and raise CopyRequestError.
        """
        db_queue_url = uuid.uuid4().__str__()
        max_retries = 2
        retry_sleep_secs = randint(0, 9999)

        file0_job_id = uuid.uuid4().__str__()
        file0_granule_id = uuid.uuid4().__str__()
        file0_input_filename = uuid.uuid4().__str__()
        file0_source_bucket = uuid.uuid4().__str__()
        file0_source_key = uuid.uuid4().__str__()
        file0_target_bucket = uuid.uuid4().__str__()
        file0_target_key = uuid.uuid4().__str__()
        error_message = uuid.uuid4().__str__()

        file1_job_id = uuid.uuid4().__str__()
        file1_granule_id = uuid.uuid4().__str__()
        file1_input_filename = uuid.uuid4().__str__()
        file1_source_bucket = uuid.uuid4().__str__()
        file1_source_key = uuid.uuid4().__str__()
        file1_target_bucket = uuid.uuid4().__str__()
        file1_target_key = uuid.uuid4().__str__()

        mock_records = Mock()

        failed_file = {
            copy_files_to_archive.INPUT_JOB_ID_KEY: file0_job_id,
            copy_files_to_archive.INPUT_GRANULE_ID_KEY: file0_granule_id,
            copy_files_to_archive.INPUT_FILENAME_KEY: file0_input_filename,
            copy_files_to_archive.FILE_SUCCESS_KEY: False,
            copy_files_to_archive.INPUT_SOURCE_BUCKET_KEY: file0_source_bucket,
            copy_files_to_archive.INPUT_SOURCE_KEY_KEY: file0_source_key,
            copy_files_to_archive.INPUT_TARGET_BUCKET_KEY: file0_target_bucket,
            copy_files_to_archive.INPUT_TARGET_KEY_KEY: file0_target_key
        }
        successful_file = {
            copy_files_to_archive.INPUT_JOB_ID_KEY: file1_job_id,
            copy_files_to_archive.INPUT_GRANULE_ID_KEY: file1_granule_id,
            copy_files_to_archive.INPUT_FILENAME_KEY: file1_input_filename,
            copy_files_to_archive.FILE_SUCCESS_KEY: False,
            copy_files_to_archive.INPUT_SOURCE_BUCKET_KEY: file1_source_bucket,
            copy_files_to_archive.INPUT_SOURCE_KEY_KEY: file1_source_key,
            copy_files_to_archive.INPUT_TARGET_BUCKET_KEY: file1_target_bucket,
            copy_files_to_archive.INPUT_TARGET_KEY_KEY: file1_target_key
        }
        mock_get_files_from_records.return_value = [failed_file, successful_file]
        mock_copy_object.side_effect = [error_message, None, error_message, error_message]

        try:
            copy_files_to_archive.task(mock_records, max_retries, retry_sleep_secs, db_queue_url)
        except copy_files_to_archive.CopyRequestError:
            mock_get_files_from_records.assert_called_once_with(mock_records)
            mock_boto3_client.assert_called_once_with('s3')
            mock_copy_object.assert_has_calls([
                call(mock_boto3_client.return_value, file0_source_bucket, file0_source_key, file0_target_bucket,
                     file0_target_key),
                call(mock_boto3_client.return_value, file1_source_bucket, file1_source_key, file1_target_bucket,
                     file1_target_key),
                call(mock_boto3_client.return_value, file0_source_bucket, file0_source_key, file0_target_bucket,
                     file0_target_key)
            ])
            self.assertEqual(3, mock_copy_object.call_count)
            mock_post_status_for_file_to_queue.assert_has_calls([
                call(file1_job_id, file1_granule_id, file1_input_filename, None, None,
                     copy_files_to_archive.ORCA_STATUS_SUCCESS, None, None,
                     mock.ANY, mock.ANY,
                     copy_files_to_archive.RequestMethod.PUT, db_queue_url, max_retries, retry_sleep_secs),
                call(file0_job_id, file0_granule_id, file0_input_filename, None, None,
                     copy_files_to_archive.ORCA_STATUS_FAILED, error_message, None,
                     mock.ANY, mock.ANY,
                     copy_files_to_archive.RequestMethod.PUT, db_queue_url, max_retries, retry_sleep_secs)
            ])
            self.assertEqual(max_retries, mock_post_status_for_file_to_queue.call_count)
            mock_sleep.assert_has_calls([call(retry_sleep_secs), call(retry_sleep_secs)])
            self.assertEqual(max_retries, mock_sleep.call_count)
            return
        self.fail('Error not raised.')

    def test_get_files_from_records_adds_success_key(self):
        """
        Function should transform json into file dict, and add 'success' key.
        """
        result = copy_files_to_archive.get_files_from_records([
            {'body': '{"key": "value0", "another_key": 5}'}, {'body': '{"key": "value1", "another_key": 15}'}])

        self.assertEqual([
            {'key': 'value0', 'another_key': 5, copy_files_to_archive.FILE_SUCCESS_KEY: False},
            {'key': 'value1', 'another_key': 15, copy_files_to_archive.FILE_SUCCESS_KEY: False}],
            result)

    def test_copy_object_happy_path(self):
        src_bucket_name = uuid.uuid4().__str__()
        src_object_name = uuid.uuid4().__str__()
        dest_bucket_name = uuid.uuid4().__str__()
        dest_object_name = uuid.uuid4().__str__()

        mock_s3_cli = Mock()

        result = copy_files_to_archive.copy_object(mock_s3_cli, src_bucket_name, src_object_name, dest_bucket_name,
                                                   dest_object_name)

        mock_s3_cli.copy_object.assert_called_once_with(CopySource={'Bucket': src_bucket_name, 'Key': src_object_name},
                                                        Bucket=dest_bucket_name,
                                                        Key=dest_object_name)
        self.assertIsNone(result)

    def test_copy_object_client_error_returned_as_string(self):
        """
        If copying the object fails, return error as string.
        """
        src_bucket_name = uuid.uuid4().__str__()
        src_object_name = uuid.uuid4().__str__()
        dest_bucket_name = uuid.uuid4().__str__()
        dest_object_name = uuid.uuid4().__str__()
        expected_result = uuid.uuid4().__str__()

        mock_s3_cli = Mock()
        error = ClientError({'Error': {}}, 'operation name')
        error.__str__ = Mock()
        error.__str__.return_value = expected_result
        mock_s3_cli.copy_object.side_effect = error

        result = copy_files_to_archive.copy_object(mock_s3_cli, src_bucket_name, src_object_name, dest_bucket_name,
                                                   dest_object_name)

        mock_s3_cli.copy_object.assert_called_once_with(CopySource={'Bucket': src_bucket_name, 'Key': src_object_name},
                                                        Bucket=dest_bucket_name,
                                                        Key=dest_object_name)
        self.assertEqual(expected_result, result)



if __name__ == '__main__':
    unittest.main(argv=['start'])