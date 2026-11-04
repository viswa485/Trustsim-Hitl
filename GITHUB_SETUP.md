# GitHub and local workflow

Clone the repository and create a virtual environment:

```bash
git clone https://github.com/viswa485/Trustsim-Hitl.git
cd Trustsim-Hitl
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
python -m pip install -e ".[dev]"
pytest
trustsim run --episodes 100 --seed 2026 --output-dir results/local-run
```

Do not commit generated results, participant data, credentials, simulator binaries or licensed engine assets. See the README and `docs/` for research boundaries and integration plans.
