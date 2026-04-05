<p align="center">
  <strong><code>dotenv-secrets</code></strong><br>
  <em>Validate, generate, and manage .env files -- catch leaked secrets before you commit.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python_3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-2ea44f?style=for-the-badge&logo=opensourceinitiative" alt="License">
  <img src="https://img.shields.io/badge/Dependencies-None-ff69b4?style=for-the-badge" alt="Zero deps">
</p>

---

## What It Does

Scans your `.env` files for leaked secrets, bad formatting, and empty values. Generates random secrets for development. Creates `.env` templates from key lists.

## Quick Start

### Validate a .env file

```bash
python -m dotenv_secrets validate .env
```

```
Validating .env...
  line 7: key 'api_key' does not match [A-Z_][A-Z0-9_]*
  line 12: key 'DATABASE_URL' contains what looks like a real secret -- use a placeholder
```

### Generate a secret

```bash
python -m dotenv_secrets secret       # 32 chars
python -m dotenv_secrets secret 64    # 64 chars
```

### Create a .env template

```bash
python -m dotenv_secrets template DATABASE_URL,SECRET_KEY,API_TOKEN .env.example
```

```
Template written to .env.example
```

## Why

- `.env` files end up in git more often than you think
- Real API keys and secrets should never be committed
- Team members need consistent variable names (UPPER_SNAKE_CASE)
- This tool catches it before it's in a PR

## Rules

| Check | What |
|---|---|
| Key format | Must match [A-Z_][A-Z0-9_]* |
| Empty values | Flags missing values after = |
| Real secrets | Detects sk-, ghp_, AKIA prefixes |
| Key syntax | Requires = separator |

## License

MIT

<p align="center">
  <a href="https://github.com/pookdkjfjdj-create">@pookdkjfjdj-create</a>
</p>
