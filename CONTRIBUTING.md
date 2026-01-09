# Contributing to 27z-6 Role Evaluator

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the project.

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Code Standards](#code-standards)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Project Structure](#project-structure)

---

## 🤝 Code of Conduct

### Our Standards

- Be respectful and inclusive
- Focus on constructive feedback
- Assume good intentions
- Prioritize evidence-based decisions
- Maintain privacy and safety standards

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Basic understanding of Python and data pipelines

### Setup Development Environment

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/27z-6_role_evaluator.git
   cd 27z-6_role_evaluator
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements-dev.txt
   ```

4. **Install pre-commit hooks (optional but recommended):**
   ```bash
   pre-commit install
   ```

5. **Verify setup:**
   ```bash
   pytest
   python tools/risk_assessment.py --help
   ```

---

## 🔄 Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

**Branch naming conventions:**
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions or updates

### 2. Make Your Changes

- Write clear, focused commits
- Follow the code standards (see below)
- Add tests for new functionality
- Update documentation as needed

### 3. Test Your Changes

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=tools --cov-report=html

# Format code
black tools/

# Check types
mypy tools/

# Lint code
flake8 tools/
```

### 4. Commit Your Changes

```bash
git add .
git commit -m "Brief description of changes

- Detailed point 1
- Detailed point 2
- Fixes #issue_number (if applicable)"
```

**Commit message guidelines:**
- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- First line should be 50 characters or less
- Reference issues and pull requests when relevant

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:
- Clear title and description
- Reference to related issues
- Screenshots (if UI changes)
- Test results

---

## 📏 Code Standards

### Python Style

We follow [PEP 8](https://pep8.org/) with some modifications:

- **Line length:** 100 characters (configured in pyproject.toml)
- **Formatter:** Black (automatic formatting)
- **Import sorting:** isort
- **Type hints:** Encouraged but not required for all functions

### Code Formatting

**Before committing, run:**
```bash
# Format code
black tools/

# Sort imports
isort tools/

# Check formatting
black --check tools/
```

### Type Hints

Add type hints to new functions:

```python
def load_csv(path: str) -> List[Dict[str, str]]:
    """Load CSV file and return list of dictionaries."""
    with open(path, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))
```

### Docstrings

Use clear docstrings for functions and classes:

```python
def haversine_km(coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
    """
    Calculate the great circle distance between two points on Earth.
    
    Args:
        coord1: Tuple of (latitude, longitude) for first point
        coord2: Tuple of (latitude, longitude) for second point
    
    Returns:
        Distance in kilometers
    
    Example:
        >>> haversine_km((47.6062, -122.3321), (47.6205, -122.3493))
        1.234
    """
    # Implementation...
```

### Error Handling

Always handle errors gracefully:

```python
# Good
try:
    data = load_csv(path)
except FileNotFoundError:
    print(f"Error: File not found: {path}")
    return []
except Exception as e:
    print(f"Error loading CSV: {e}")
    return []

# Bad
data = load_csv(path)  # Could crash with no explanation
```

---

## 🧪 Testing

### Writing Tests

Tests go in the `tests/` directory:

```
tests/
├── test_data_validation.py
├── test_risk_assessment.py
└── test_geocoding.py
```

**Example test:**
```python
import pytest
from tools.risk_assessment import to_int

def test_to_int_valid():
    assert to_int("42") == 42
    assert to_int("3.14") == 3

def test_to_int_invalid():
    assert to_int("") == 0
    assert to_int(None) == 0
    assert to_int("abc") == 0
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_risk_assessment.py

# Run with coverage
pytest --cov=tools --cov-report=html

# Run with verbose output
pytest -v
```

### Test Coverage

Aim for reasonable test coverage:
- Critical functions: 80%+ coverage
- Data validation: High coverage
- CLI tools: Basic integration tests

---

## 📤 Submitting Changes

### Pull Request Checklist

Before submitting a PR, ensure:

- [ ] Code follows style guidelines (Black, isort)
- [ ] All tests pass (`pytest`)
- [ ] New tests added for new functionality
- [ ] Documentation updated (if needed)
- [ ] Commit messages are clear and descriptive
- [ ] No sensitive data or credentials in code
- [ ] Changes are focused and atomic

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring
- [ ] Other (please describe)

## Testing
- [ ] All existing tests pass
- [ ] New tests added
- [ ] Manual testing completed

## Related Issues
Fixes #issue_number

## Screenshots (if applicable)
[Add screenshots here]
```

---

## 📁 Project Structure

### Key Directories

- **`tools/`** - Python data pipeline and CLI scripts
- **`data/`** - Data files (raw, normalized, exports)
- **`app/`** - Static web application (map UI)
- **`scripts/`** - Wrapper scripts for common tasks
- **`docs/`** - Project documentation
- **`tests/`** - Test files

### Adding New Features

#### New Data Export Script

1. Create `tools/export_new_feature.py`
2. Follow existing export script patterns
3. Add to `scripts/build_map_data.bat` if needed
4. Document in README.md

#### New CLI Feature

1. Update `tools/risk_assessment.py`
2. Add argparse options
3. Add tests in `tests/test_risk_assessment.py`
4. Update documentation

#### New Map Feature

1. Update `app/public/index.html`
2. Test locally with `scripts/run_map.ps1`
3. Document in `docs/UI_WIREFRAME.md`

---

## 🐛 Reporting Bugs

### Before Reporting

1. Check existing issues
2. Verify you're using the latest version
3. Test with a clean virtual environment

### Bug Report Template

```markdown
**Describe the bug**
Clear description of what the bug is

**To Reproduce**
Steps to reproduce:
1. Run command '...'
2. See error

**Expected behavior**
What you expected to happen

**Environment:**
- OS: [e.g., Windows 10]
- Python version: [e.g., 3.9.7]
- Project version: [e.g., v1.0-internal]

**Additional context**
Any other relevant information
```

---

## 💡 Feature Requests

We welcome feature requests! Please:

1. Check if the feature already exists or is planned
2. Describe the use case clearly
3. Explain why it aligns with project goals
4. Consider submitting a PR if you can implement it

---

## 📞 Questions?

- Check the [documentation](docs/)
- Review existing issues and PRs
- Open a new issue with the "question" label

---

## 🙏 Thank You!

Your contributions help make this project better for everyone. We appreciate your time and effort!

---

**Remember:** This project prioritizes evidence-based decisions, privacy, and safety. All contributions should align with these principles.
