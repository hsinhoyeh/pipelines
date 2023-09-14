"""AutoML Feature Transform Engine component spec."""

# Copyright 2023 The Kubeflow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Optional

from kfp import dsl


@dsl.container_component
def distillation_stage_feature_transform_engine(
    root_dir: str,
    project: str,
    location: str,
    transform_config_path: str,
    bigquery_train_full_table_uri: str,
    bigquery_validate_full_table_uri: str,
    target_column: str,
    prediction_type: str,
    materialized_data: dsl.Output[dsl.Dataset],
    transform_output: dsl.Output[dsl.Artifact],
    gcp_resources: dsl.OutputPath(str),
    bigquery_staging_full_dataset_id: Optional[str] = '',
    weight_column: Optional[str] = '',
    dataflow_machine_type: Optional[str] = 'n1-standard-16',
    dataflow_max_num_workers: Optional[int] = 25,
    dataflow_disk_size_gb: Optional[int] = 40,
    dataflow_subnetwork: Optional[str] = '',
    dataflow_use_public_ips: Optional[bool] = True,
    dataflow_service_account: Optional[str] = '',
    encryption_spec_key_name: Optional[str] = '',
    autodetect_csv_schema: Optional[bool] = False,
):
  # fmt: off
  """Feature Transform Engine (FTE) component to transform raw data to engineered features during model distilation.

  The FTE transform configuration is generated as part of the FTE stage prior
  to distillation.  This distillation-stage FTE component re-uses this config to
  transform the input datasets with predicted outputs included (soft targets).

  Args:
    root_dir: The Cloud Storage location to store the output.
    project: Project to run feature transform engine.
    location: Location for the created GCP services.
    transform_config_path: Path to the transform config output by the pre-distillation FTE component.
    bigquery_train_full_table_uri: BigQuery full table id for our train split output by pre-distillation FTE with soft target included.
    bigquery_validate_full_table_uri: BigQuery full table id for our validation split output by pre-distillation FTE with soft target included.
    target_column: Target column of input data. prediction_type (str): Model prediction type. One of "classification", "regression", "time_series".
    bigquery_staging_full_dataset_id: Dataset in 'projectId.datasetId' format for storing intermediate-FTE BigQuery tables.  If the specified dataset does not exist in BigQuery, FTE will create the dataset. If no bigquery_staging_full_dataset_id is specified, all intermediate tables will be stored in a dataset created under the provided project in the input data source's location during FTE execution called 'vertex_feature_transform_engine_staging_{location.replace('-', '_')}'. All tables generated by FTE will have a 30 day TTL.
    weight_column: Weight column of input data.
    dataflow_machine_type: The machine type used for dataflow jobs. If not set, default to n1-standard-16.
    dataflow_max_num_workers: The number of workers to run the dataflow job. If not set, default to 25.
    dataflow_disk_size_gb: The disk size, in gigabytes, to use on each Dataflow worker instance. If not set, default to 40.
    dataflow_subnetwork: Dataflow's fully qualified subnetwork name, when empty the default subnetwork will be used. More details: https://cloud.google.com/dataflow/docs/guides/specifying-networks#example_network_and_subnetwork_specifications dataflow_use_public_ips (Optional[bool]): Specifies whether Dataflow workers use public IP addresses.
    dataflow_service_account: Custom service account to run Dataflow jobs.
    encryption_spec_key_name: Customer-managed encryption key.

  Returns:
    materialized_data: The materialized dataset.
    transform_output: The transform output artifact.
    gcp_resources: GCP resources created by this component. For more details, see https://github.com/kubeflow/pipelines/blob/master/components/google-cloud/google_cloud_pipeline_components/proto/README.md.
  """
  # fmt: on

  return dsl.ContainerSpec(
      image='us-docker.pkg.dev/vertex-ai/automl-tabular/feature-transform-engine:20230910_1325',
      command=[],
      args=[
          'distillation_stage_feature_transform_engine',
          dsl.ConcatPlaceholder(items=['--project=', project]),
          dsl.ConcatPlaceholder(items=['--location=', location]),
          dsl.ConcatPlaceholder(
              items=[
                  '--transform_config_path=',
                  transform_config_path,
              ]
          ),
          dsl.ConcatPlaceholder(
              items=[
                  '--bigquery_train_full_table_uri=',
                  bigquery_train_full_table_uri,
              ]
          ),
          dsl.ConcatPlaceholder(
              items=[
                  '--bigquery_validate_full_table_uri=',
                  bigquery_validate_full_table_uri,
              ]
          ),
          dsl.ConcatPlaceholder(
              items=[
                  '--bigquery_staging_full_dataset_id=',
                  bigquery_staging_full_dataset_id,
              ]
          ),
          dsl.ConcatPlaceholder(items=['--target_column=', target_column]),
          dsl.ConcatPlaceholder(items=['--prediction_type=', prediction_type]),
          dsl.ConcatPlaceholder(items=['--weight_column=', weight_column]),
          dsl.ConcatPlaceholder(
              items=[
                  '--error_file_path=',
                  root_dir,
                  f'/{dsl.PIPELINE_JOB_ID_PLACEHOLDER}/{dsl.PIPELINE_TASK_ID_PLACEHOLDER}/error.txt',
              ]
          ),
          dsl.ConcatPlaceholder(
              items=[
                  '--transform_output_artifact_path=',
                  transform_output.uri,
              ]
          ),
          dsl.ConcatPlaceholder(
              items=[
                  '--transform_output_path=',
                  root_dir,
                  f'/{dsl.PIPELINE_JOB_ID_PLACEHOLDER}/{dsl.PIPELINE_TASK_ID_PLACEHOLDER}/transform',
              ]
          ),
          dsl.ConcatPlaceholder(
              items=[
                  '--materialized_examples_path=',
                  root_dir,
                  f'/{dsl.PIPELINE_JOB_ID_PLACEHOLDER}/{dsl.PIPELINE_TASK_ID_PLACEHOLDER}/materialized',
              ]
          ),
          dsl.ConcatPlaceholder(
              items=[
                  '--export_data_path=',
                  root_dir,
                  f'/{dsl.PIPELINE_JOB_ID_PLACEHOLDER}/{dsl.PIPELINE_TASK_ID_PLACEHOLDER}/export',
              ]
          ),
          dsl.ConcatPlaceholder(
              items=[
                  '--materialized_data_path=',
                  root_dir,
                  f'/{dsl.PIPELINE_JOB_ID_PLACEHOLDER}/{dsl.PIPELINE_TASK_ID_PLACEHOLDER}/materialized_data',
              ]
          ),
          dsl.ConcatPlaceholder(
              items=[
                  '--materialized_data_artifact_path=',
                  materialized_data.uri,
              ]
          ),
          f'--job_name=feature-transform-engine-{dsl.PIPELINE_JOB_ID_PLACEHOLDER}-{dsl.PIPELINE_TASK_ID_PLACEHOLDER}',
          dsl.ConcatPlaceholder(items=['--dataflow_project=', project]),
          dsl.ConcatPlaceholder(
              items=[
                  '--dataflow_staging_dir=',
                  root_dir,
                  f'/{dsl.PIPELINE_JOB_ID_PLACEHOLDER}/{dsl.PIPELINE_TASK_ID_PLACEHOLDER}/dataflow_staging',
              ]
          ),
          dsl.ConcatPlaceholder(
              items=[
                  '--dataflow_tmp_dir=',
                  root_dir,
                  f'/{dsl.PIPELINE_JOB_ID_PLACEHOLDER}/{dsl.PIPELINE_TASK_ID_PLACEHOLDER}/dataflow_tmp',
              ]
          ),
          dsl.ConcatPlaceholder(
              items=[
                  '--dataflow_max_num_workers=',
                  dataflow_max_num_workers,
              ]
          ),
          dsl.ConcatPlaceholder(
              items=[
                  '--dataflow_machine_type=',
                  dataflow_machine_type,
              ]
          ),
          '--dataflow_worker_container_image=us-docker.pkg.dev/vertex-ai/automl-tabular/dataflow-worker:20230910_1325',
          dsl.ConcatPlaceholder(
              items=[
                  '--dataflow_disk_size_gb=',
                  dataflow_disk_size_gb,
              ]
          ),
          dsl.ConcatPlaceholder(
              items=[
                  '--dataflow_subnetwork_fully_qualified=',
                  dataflow_subnetwork,
              ]
          ),
          dsl.ConcatPlaceholder(
              items=[
                  '--dataflow_use_public_ips=',
                  dataflow_use_public_ips,
              ]
          ),
          dsl.ConcatPlaceholder(
              items=[
                  '--dataflow_service_account=',
                  dataflow_service_account,
              ]
          ),
          dsl.ConcatPlaceholder(
              items=[
                  '--dataflow_kms_key=',
                  encryption_spec_key_name,
              ]
          ),
          dsl.ConcatPlaceholder(items=['--gcp_resources_path=', gcp_resources]),
      ],
  )
