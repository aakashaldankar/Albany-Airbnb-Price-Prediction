import shutil
import subprocess
from pathlib import Path
import pytest
import yaml

@pytest.mark.integration
@pytest.mark.slow
def test_dvc_pipeline_runs_in_temp_workspace(tmp_path):
    
    project_root = Path(__file__).resolve().parents[2]
    temp_project = tmp_path / "project"

    ignore = shutil.ignore_patterns(
        ".dvc/cache",
        "__pycache__",
        ".pytest_cache",
        "htmlcov",
        "mlruns",
        "central_data",
        "experiments",
        "models",
        "metrics",
        "reports",
    )

    shutil.copytree(project_root, temp_project, ignore=ignore)

    params = {
          "data_ingestion": {"test_size": 0.3, "data_url": 'https://raw.githubusercontent.com/aakashaldankar/Albany-Airbnb-Listings-Data/refs/heads/main/listings.csv'},
          "feature_engineering": {"max_features": 5},
          "model_training": {
              "hyper_parameters": {
                  "n_estimators": 2,
                  "max_depth": 2,
                  "learning_rate": 0.1,
                  "subsample": 0.8,
              }
          },
          "tracking_uri": f"file://{tmp_path / 'mlruns'}",
      }

    with open(temp_project/"params.yaml", "w") as f:
        yaml.safe_dump(params, f)

    result = subprocess.run(
        ["dvc", "repro"],
        cwd=temp_project,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stderr

    assert (temp_project / "central_data/raw_data/train_data.csv").exists()
    assert (temp_project / "central_data/pre_processed/pre_processed_train.csv").exists()
    assert (temp_project / "central_data/feature_engineering/final_train_data.csv").exists()
    assert (temp_project / "src/feature_encoders/feature_engineering_encoders.pkl").exists()
