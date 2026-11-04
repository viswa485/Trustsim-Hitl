# Contributing

Contributions should preserve reproducibility, provenance and the safety boundary of this prototype.

## Development

```bash
python -m pip install -e ".[dev]"
pytest
ruff check .
```

## Expectations

- Document research assumptions and changes to metric definitions.
- Add tests for behavioural changes.
- Preserve deterministic seeds where practical.
- Never label synthetic proxy labels as human feedback.
- Do not commit participant data, credentials, simulator binaries or licensed engine assets.
- Record exact versions and licence review before adding third-party code, assets or datasets.
- Include command, seed, episode count, versions, uncertainty and limitations when reporting results.
