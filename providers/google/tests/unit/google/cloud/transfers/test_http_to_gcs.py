#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
from __future__ import annotations

from unittest import mock

from airflow.providers.google.cloud.transfers.http_to_gcs import HttpToGCSOperator

TASK_ID = "test-http-to-gcs-operator"
GCP_CONN_ID = "GCP_CONN_ID"
HTTP_CONN_ID = "HTTP_CONN_ID"
IMPERSONATION_CHAIN = ["ACCOUNT_1", "ACCOUNT_2", "ACCOUNT_3"]

TEST_BUCKET = "test-bucket"
DESTINATION_PATH_FILE = "destination_dir/copy.txt"
ENDPOINT = "/"
HEADERS = {"header_key": "header_value"}
DATA = {"some": "data"}
EXTRA_OPTIONS = {"check_response": False}
DEFAULT_HTTP_METHOD = "GET"
NUM_MAX_ATTEMPTS = 3
TCP_KEEP_ALIVE_IDLE = 120
TCP_KEEP_ALIVE_COUNT = 20
TCP_KEEP_ALIVE_INTERVAL = 30


class TestHttpToGCSOperator:
    def test_init(self):
        operator = HttpToGCSOperator(
            task_id="http_to_gcs_operator",
            http_conn_id=HTTP_CONN_ID,
            endpoint=ENDPOINT,
            object_name=DESTINATION_PATH_FILE,
            bucket_name=TEST_BUCKET,
        )
        assert operator.endpoint == ENDPOINT
        assert operator.object_name == DESTINATION_PATH_FILE
        assert operator.bucket_name == TEST_BUCKET
        assert operator.http_conn_id == HTTP_CONN_ID

    @mock.patch("airflow.providers.google.cloud.transfers.http_to_gcs.GCSHook")
    @mock.patch("airflow.providers.google.cloud.transfers.http_to_gcs.HttpHook")
    def test_execute_copy_single_file(self, http_hook, gcs_hook):
        task = HttpToGCSOperator(
            task_id="http_to_gcs_operator",
            http_conn_id=HTTP_CONN_ID,
            endpoint=ENDPOINT,
            headers=HEADERS,
            data=DATA,
            extra_options=EXTRA_OPTIONS,
            object_name=DESTINATION_PATH_FILE,
            bucket_name=TEST_BUCKET,
            gcp_conn_id=GCP_CONN_ID,
            impersonation_chain=IMPERSONATION_CHAIN,
        )
        task.execute(None)
