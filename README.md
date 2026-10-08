# mlops-end-to-end

A search query parser that tags each token as `author`, `category`, `format` or `other`.
The model is deliberately simple; the point is the MLOps around it. All data is fake.

## Quick start

```bash
uv sync          # base + dev deps
make test
make setup       # everything (mlflow, dvc, fastapi, evidently)
```

## Layout

| Path | What | Phase |
|---|---|---|
| `src/query_parser/` | generate_data, train, evaluate, app, drift | 1-3 |
| `params.yaml` | settings for every pipeline stage | 1 |
| `data/raw`, `data/processed`, `data/golden` | DVC-tracked data (S3 remote) | 1 |
| `models/` | trained model artifacts (DVC-tracked) | 1 |
| `k8s/base`, `k8s/overlays/{kind,eks}` | Kustomize manifests, HPA, KEDA, Argo Rollouts | 2 |
| `k8s/monitoring/` | Prometheus / Grafana | 2 |
| `loadtest/` | k6 scripts | 2 |
| `airflow/dags/` | retraining DAG triggered by drift alert | 3 |
| `infra/terraform/` | VPC, EKS, ECR, S3, IAM, Karpenter | 4 |
| `.github/workflows/` | CI now; OIDC deploy to AWS in phase 5 | 5 |
| `notebooks/` | scratch exploration | - |

## Phases

1. Fake data + DVC, training + MLflow, golden-set gate
2. Local kind: HPA, KEDA, Argo Rollouts canary, Prometheus/Grafana, k6
3. Evidently drift CronJob -> Airflow retraining DAG
4. AWS with Terraform (EKS, Karpenter on spot)
5. GitHub Actions with OIDC to AWS
6. SageMaker serverless deploy for comparison
