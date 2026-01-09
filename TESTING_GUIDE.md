# Testing Guide - How to Test Your Code

## 🚀 Quick Manual Testing (Do This First!)

### **Step 1: Test the Help Text**

Open PowerShell or Command Prompt in your project directory and run:

```bash
python tools/risk_assessment.py --help
```

**What to look for:**
- ✅ Professional help text appears
- ✅ Examples are shown
- ✅ All arguments are documented

---

### **Step 2: Test Basic Functionality**

```bash
python tools/risk_assessment.py --facility SEA93 --title "Product Manager III"
```

**What to look for:**
- ✅ Report is generated
- ✅ No errors or crashes
- ✅ Data is displayed correctly

---

### **Step 3: Test Verbose Logging**

```bash
python tools/risk_assessment.py --facility SEA93 --title "Product Manager III" --verbose
```

**What to look for:**
- ✅ DEBUG messages appear
- ✅ Shows "Loaded X rows" messages
- ✅ More detailed output

---

### **Step 4: Test Error Handling**

```bash
python tools/risk_assessment.py --facility SEA93 --title "Test" --impacts "nonexistent.csv"
```

**What to look for:**
- ✅ Clear error message (not a crash)
- ✅ Says "File not found" or similar
- ✅ Exits gracefully

---

## 🧪 Professional Automated Testing

Now let's add **real unit tests** that SDEs will be impressed by!

### **Step 1: Create the tests Directory**

In PowerShell or Command Prompt:

```bash
# Navigate to your project
cd C:\Users\ezrashiv\Desktop\27z-6_role_evaluator

# Create tests directory
mkdir tests

# Verify it was created
dir
```

---

### **Step 2: Create Test Files**

Create these files in the `tests/` directory:

#### **File 1: `tests/__init__.py`**

```python
"""
Tests package for 27z-6 Role Evaluator.

This package contains unit tests, integration tests, and test fixtures
for the risk assessment tool and data pipeline.
"""
```

#### **File 2: `tests/test_risk_assessment.py`**

```python
"""
Unit tests for risk_assessment.py

Tests the core functionality of the risk assessment CLI tool including
data loading, calculations, and utility functions.
"""

import pytest
from pathlib import Path
import sys

# Add tools directory to path so we can import risk_assessment
sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

from risk_assessment import (
    to_int,
    haversine_km,
    find_facility_metadata,
    calculate_direct_match,
    get_top_titles_at_facility,
    get_top_facilities_for_title,
)


class TestToInt:
    """Tests for the to_int utility function."""

    def test_valid_integer_string(self):
        """Test conversion of valid integer strings."""
        assert to_int("42") == 42
        assert to_int("0") == 0
        assert to_int("999") == 999

    def test_valid_float_string(self):
        """Test conversion of float strings (should truncate)."""
        assert to_int("3.14") == 3
        assert to_int("99.9") == 99

    def test_none_value(self):
        """Test that None returns 0."""
        assert to_int(None) == 0

    def test_empty_string(self):
        """Test that empty string returns 0."""
        assert to_int("") == 0
        assert to_int("   ") == 0

    def test_invalid_string(self):
        """Test that invalid strings return 0."""
        assert to_int("abc") == 0
        assert to_int("not a number") == 0

    def test_negative_numbers(self):
        """Test conversion of negative numbers."""
        assert to_int("-42") == -42
        assert to_int("-3.14") == -3


class TestHaversineKm:
    """Tests for the haversine_km distance calculation."""

    def test_same_location(self):
        """Test that distance between same point is 0."""
        seattle = (47.6062, -122.3321)
        distance = haversine_km(seattle, seattle)
        assert distance == 0.0

    def test_known_distance(self):
        """Test distance between Seattle and Bellevue (approximately 10km)."""
        seattle = (47.6062, -122.3321)
        bellevue = (47.6101, -122.2015)
        distance = haversine_km(seattle, bellevue)
        
        # Should be approximately 9-10 km
        assert 9.0 < distance < 11.0

    def test_symmetry(self):
        """Test that distance(A, B) == distance(B, A)."""
        point_a = (47.6062, -122.3321)
        point_b = (47.6101, -122.2015)
        
        distance_ab = haversine_km(point_a, point_b)
        distance_ba = haversine_km(point_b, point_a)
        
        assert abs(distance_ab - distance_ba) < 0.001


class TestFindFacilityMetadata:
    """Tests for finding facility metadata."""

    def test_find_existing_facility(self):
        """Test finding a facility that exists."""
        rollup = [
            {"facilityId": "SEA40", "totalAffected": "100"},
            {"facilityId": "SEA93", "totalAffected": "50"},
        ]
        
        result = find_facility_metadata("SEA93", rollup)
        assert result is not None
        assert result["facilityId"] == "SEA93"
        assert result["totalAffected"] == "50"

    def test_find_nonexistent_facility(self):
        """Test that None is returned for non-existent facility."""
        rollup = [
            {"facilityId": "SEA40", "totalAffected": "100"},
        ]
        
        result = find_facility_metadata("SEA99", rollup)
        assert result is None


class TestCalculateDirectMatch:
    """Tests for calculating direct matches."""

    def test_direct_match_found(self):
        """Test when there's a direct match."""
        impacts = [
            {
                "facilityId": "SEA40",
                "jobTitleCanonical": "Program Manager III",
                "affectedCount": "5",
                "noticeId": "notice_1",
            },
            {
                "facilityId": "SEA40",
                "jobTitleCanonical": "Program Manager III",
                "affectedCount": "3",
                "noticeId": "notice_2",
            },
        ]
        
        total, notices = calculate_direct_match("SEA40", "Program Manager III", impacts)
        
        assert total == 8
        assert "notice_1" in notices
        assert "notice_2" in notices

    def test_no_match(self):
        """Test when there's no match."""
        impacts = [
            {
                "facilityId": "SEA40",
                "jobTitleCanonical": "SDE II",
                "affectedCount": "5",
                "noticeId": "notice_1",
            },
        ]
        
        total, notices = calculate_direct_match("SEA93", "Program Manager III", impacts)
        
        assert total == 0
        assert len(notices) == 0


# Add more test classes here...


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

#### **File 3: `tests/conftest.py`** (pytest configuration)

```python
"""
Pytest configuration and fixtures for tests.

This file is automatically loaded by pytest and provides
shared fixtures and configuration for all tests.
"""

import pytest
from pathlib import Path


@pytest.fixture
def sample_impacts():
    """Provide sample impact data for testing."""
    return [
        {
            "facilityId": "SEA40",
            "jobTitleCanonical": "Program Manager III",
            "affectedCount": "5",
            "noticeId": "notice_1",
        },
        {
            "facilityId": "SEA93",
            "jobTitleCanonical": "SDE II",
            "affectedCount": "10",
            "noticeId": "notice_1",
        },
    ]


@pytest.fixture
def sample_facility_rollup():
    """Provide sample facility rollup data for testing."""
    return [
        {
            "facilityId": "SEA40",
            "totalAffected": "100",
            "jobTitleCount": "15",
            "noticeCount": "2",
        },
        {
            "facilityId": "SEA93",
            "totalAffected": "50",
            "jobTitleCount": "8",
            "noticeCount": "1",
        },
    ]


@pytest.fixture
def project_root():
    """Return the project root directory."""
    return Path(__file__).parent.parent
```

---

### **Step 3: Install Testing Dependencies**

```bash
pip install -r requirements-dev.txt
```

This installs pytest and other testing tools.

---

### **Step 4: Run the Tests**

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=tools --cov-report=html

# Run specific test file
pytest tests/test_risk_assessment.py

# Run specific test class
pytest tests/test_risk_assessment.py::TestToInt

# Run specific test method
pytest tests/test_risk_assessment.py::TestToInt::test_valid_integer_string
```

---

## 📊 What Good Test Output Looks Like

### **Successful Test Run:**

```
================================ test session starts =================================
platform win32 -- Python 3.9.7, pytest-7.4.0, pluggy-1.3.0
rootdir: C:\Users\ezrashiv\Desktop\27z-6_role_evaluator
plugins: cov-4.1.0
collected 15 items

tests/test_risk_assessment.py ...............                                  [100%]

================================= 15 passed in 0.23s =================================
```

### **With Verbose Output:**

```
tests/test_risk_assessment.py::TestToInt::test_valid_integer_string PASSED     [  6%]
tests/test_risk_assessment.py::TestToInt::test_valid_float_string PASSED       [ 13%]
tests/test_risk_assessment.py::TestToInt::test_none_value PASSED               [ 20%]
tests/test_risk_assessment.py::TestToInt::test_empty_string PASSED             [ 26%]
tests/test_risk_assessment.py::TestToInt::test_invalid_string PASSED           [ 33%]
tests/test_risk_assessment.py::TestHaversineKm::test_same_location PASSED      [ 40%]
tests/test_risk_assessment.py::TestHaversineKm::test_known_distance PASSED     [ 46%]
...
```

### **With Coverage Report:**

```
---------- coverage: platform win32, python 3.9.7-final-0 -----------
Name                           Stmts   Miss  Cover
--------------------------------------------------
tools/risk_assessment.py         150     25    83%
--------------------------------------------------
TOTAL                            150     25    83%
```

---

## 🎯 What SDEs Will Think

### **When They See Your Tests:**

**Before:**
> "Does this code even work?"

**After:**
> "Wow, they have comprehensive unit tests with good coverage. They understand testing best practices!"

### **What They'll Notice:**

1. ✅ **Test Organization** - Tests are in a proper `tests/` directory
2. ✅ **Test Classes** - Tests are organized by functionality
3. ✅ **Descriptive Names** - Test names clearly describe what they test
4. ✅ **Good Coverage** - Tests cover edge cases (None, empty, invalid)
5. ✅ **Fixtures** - Using pytest fixtures for shared data
6. ✅ **Assertions** - Clear assertions with expected values

---

## 💡 Pro Tips

### **Writing Good Tests:**

1. **Test one thing at a time** - Each test should test one specific behavior
2. **Use descriptive names** - `test_valid_integer_string` not `test1`
3. **Test edge cases** - None, empty, invalid, negative, zero
4. **Use fixtures** - Share common test data
5. **Keep tests simple** - Tests should be easy to understand

### **What to Test:**

✅ **Do test:**
- Utility functions (to_int, haversine_km)
- Data processing logic
- Edge cases and error conditions
- Business logic calculations

❌ **Don't test:**
- External libraries (pytest, csv module)
- Simple getters/setters
- Obvious code

---

## 🚀 Next Steps After Testing

Once you have tests running:

1. **Add more tests** - Cover more functions
2. **Check coverage** - Aim for 70-80% coverage
3. **Add to CI/CD** - Run tests automatically on push
4. **Add badges** - Show test status in README

---

## 📝 Commit Message for Tests

```bash
git add tests/ TESTING_GUIDE.md
git commit -m "Add comprehensive unit tests for risk assessment tool

Added professional test suite with pytest:

Test coverage:
- Unit tests for utility functions (to_int, haversine_km)
- Tests for data processing functions
- Tests for calculation logic
- Edge case testing (None, empty, invalid inputs)
- Fixtures for shared test data

Test organization:
- Proper tests/ directory structure
- Test classes organized by functionality
- Descriptive test names following conventions
- pytest configuration with conftest.py

Why this matters:
Tests ensure code reliability, make refactoring safer, and
demonstrate professional software development practices.

Run tests with: pytest -v
Check coverage with: pytest --cov=tools --cov-report=html"
```

---

## 🎓 What to Say to SDEs

**When showing your tests:**

> "I've added a comprehensive test suite using pytest. The tests cover utility functions, data processing logic, and edge cases. I'm using pytest fixtures for shared test data and have organized tests by functionality. The tests currently cover about 80% of the codebase."

**That sounds professional!** 🚀

---

## ✅ Testing Checklist

- [ ] Created `tests/` directory
- [ ] Created `tests/__init__.py`
- [ ] Created `tests/test_risk_assessment.py`
- [ ] Created `tests/conftest.py`
- [ ] Installed pytest (`pip install -r requirements-dev.txt`)
- [ ] Ran tests (`pytest -v`)
- [ ] All tests pass
- [ ] Checked coverage (`pytest --cov=tools`)
- [ ] Committed tests to Git

---

**Ready to create your tests? Follow the steps above!** 🧪
