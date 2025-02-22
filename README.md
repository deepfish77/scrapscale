# scrapscale
project-root/
├── .git/                    # Git metadata (Leave as is)
├── shared_docs/             # (Optional) Documentation, design docs, and README files
│   ├── README.md
│   └── design/
│       └── architecture.png

├── lambda_stack/            # Standard Lambda functions
│   ├── package-lock.json
│   ├── package.json
│   ├── Pipfile
│   ├── Pipfile.lock
│   ├── serverless.yml
│   ├── src/
│   │   ├── __init__.py
│   │   ├── handlers/
│   │   │   ├── handler_1.py
│   │   │   ├── handler_2.py
│   │   │   └── __init__.py
│   │   ├── models/
│   │   │   ├── models.py
│   │   │   └── __init__.py
│   │   └── utils/
│   │       ├── assume_role.py
│   │       ├── data_utils.py
│   │       ├── dynamo_utils.py
│   │       ├── enums.py
│   │       ├── rds_connect.py
│   │       ├── rds_instance.py
│   │       ├── s3_file_uploader.py
│   │       ├── sql_schemas.py
│   │       ├── __init__.py
│   │       └── generic_utils/
│   │           ├── ftp_handler_utils.py
│   │           ├── sqs_process_template.py
│   │           └── __init__.py
│   └── tests/                # Add unit tests for standard Lambda functions
│       ├── test_handler_1.py
│       └── test_utils.py

├── lambda_container_stack/   # Containerized Lambda
│   ├── dockerfile
│   ├── Pipfile
│   ├── Pipfile.lock
│   ├── requirements.txt
│   ├── serverless.yml
│   ├── src/
│   │   ├── __init__.py
│   │   ├── handlers/
│   │   │   ├── app.py
│   │   │   ├── dispatcher.py
│   │   │   └── __init__.py
│   │   ├── scapers_ops/
│   │   │   ├── get_content_fbbm.py
│   │   │   └── __init__.py
│   │   └── scrap_utils/
│   │       ├── call_wrapper.py
│   │       ├── get_all_props.py
│   │       ├── get_auth_tokens.py
│   │       ├── get_internals.py
│   │       ├── headers_from_request.py
│   │       ├── tls_client_proxy.py
│   │       └── __init__.py
│   └── tests/                # Add unit tests for containerized service
│       ├── test_app.py
│       └── test_dispatcher.py

└── ci_cd/                    # Optional: CI/CD scripts and configurations
    ├── buildspec.yml         # AWS CodeBuild or GitHub Actions scripts
    ├── deploy_container.sh
    └── deploy_lambda.sh
