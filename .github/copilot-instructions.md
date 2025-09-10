# ppup - Automated Record Keeping Tool

ppup is a Python Selenium automation tool that automates filling daily health records on pepup.life website. The tool uses Microsoft Edge WebDriver to navigate forms and submit data for step counts, sleep hours, and other health metrics.

**Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.**

## Quick Start (Essential Steps)
**NEVER CANCEL: Total setup time ~3 minutes. Set timeout to 10+ minutes.**

```bash
# 1. Check Python version (must be 3.10+)
python3 --version

# 2. Setup environment (takes ~3 seconds)
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# 3. Install dependencies (takes ~15-30 seconds)
pip install -r requirement.txt

# 4. Setup credentials
cp .env.example .env
# Edit .env with real pepup.life credentials

# 5. Download WebDriver (manual step - see WebDriver Setup section)

# 6. Run application (takes 5-10 minutes, requires manual reCAPTCHA solving)
python ppup.py
```

## Working Effectively

### Environment Setup and Dependencies
**NEVER CANCEL: Setup takes 2-3 minutes total. Set timeout to 10+ minutes.**

- Ensure Python 3.10+ is available (validated with Python 3.12.3):
  ```bash
  python3 --version  # Should show 3.10+
  ```

- Create and activate virtual environment:
  ```bash
  # Create virtual environment (takes ~3 seconds)
  python3 -m venv venv
  
  # Activate virtual environment
  # Linux/macOS:
  source venv/bin/activate
  # Windows:
  venv\Scripts\activate
  ```

- Install dependencies from requirement.txt (takes ~15-30 seconds, may timeout in restricted networks):
  ```bash
  pip install -r requirement.txt
  ```
  **NOTE**: If pip install fails with timeout errors in restricted environments, the dependencies are: selenium, python-dotenv, and their sub-dependencies.

### WebDriver Setup (CRITICAL)
**The application requires Microsoft Edge WebDriver to function.**

**Option 1: Manual WebDriver Download (Recommended for production)**
- Download Microsoft Edge WebDriver from: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
- Extract the msedgedriver.exe file to the same directory as ppup.py
- **CRITICAL**: WebDriver version must match your Edge browser version exactly

**Option 2: Auto WebDriver Management (For development/testing)**
- Install webdriver-manager: `pip install webdriver-manager`
- Modify code to use `EdgeChromiumDriverManager().install()` instead of 'msedgedriver.exe'

### Configuration Setup
- Copy .env.example to .env:
  ```bash
  cp .env.example .env
  ```
- Edit .env file with actual pepup.life credentials:
  ```
  PEPUP_EMAIL=your_actual_email@example.com
  PEPUP_PASSWORD=your_actual_password
  ```
- **CRITICAL**: Never commit .env file to repository (already in .gitignore)

### Running the Application
**NEVER CANCEL: Full execution takes 5-10 minutes depending on month length. Set timeout to 15+ minutes.**

```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Run the main application
python ppup.py
```

**MANUAL INTERACTION REQUIRED:**
- Application opens Edge browser and navigates to pepup.life login
- Fills email and password automatically
- **CRITICAL**: You have 30 seconds to manually solve reCAPTCHA
- After reCAPTCHA is solved, automation continues for entire month

## Validation and Testing

### Code Quality Checks
Always run these before committing changes:

```bash
# Activate virtual environment first
source venv/bin/activate

# Syntax check (takes ~0.1 seconds)
python -m py_compile ppup.py config.py funcs.py

# Install linting tools (takes ~20 seconds)
pip install flake8 black

# Linting check (takes ~0.4 seconds)
flake8 *.py --max-line-length=88

# Format check (takes ~0.2 seconds)
black --check *.py

# Apply formatting if needed
black *.py
```

### Functional Testing
Test utility functions without WebDriver:
```bash
python -c "
import funcs
print('getWeekday(2024, 1, 15):', funcs.getWeekday(2024, 1, 15))  # Should be 0 (Monday)
print('getLastDay(2024, 2):', funcs.getLastDay(2024, 2))        # Should be 29 (leap year)
print('getRandomInt(0, 1000):', funcs.getRandomInt(0, 1000))     # Random number 0-1000
"
```

Test configuration loading:
```bash
python -c "
import config
try:
    email, password = config.get_login_credentials()
    print('Config loaded successfully:', email)
except ValueError as e:
    print('Expected error without .env:', e)
"
```

### Manual Validation Scenarios
**CRITICAL**: Always test these scenarios after making changes:

1. **Environment Setup Test**:
   - Create fresh virtual environment
   - Install dependencies
   - Verify no import errors

2. **Configuration Test**:
   - Copy .env.example to .env
   - Add test credentials
   - Verify config.get_login_credentials() works

3. **WebDriver Test** (if WebDriver available):
   - Run application
   - Verify browser opens
   - Verify navigation to pepup.life works
   - Cancel execution after login page loads

## Codebase Structure

### Key Files
- **ppup.py** (148 lines): Main application entry point with Selenium automation logic
- **config.py** (22 lines): Environment variable loading and credential management
- **funcs.py** (15 lines): Utility functions for date calculations and random numbers
- **requirement.txt**: Python dependencies (note: singular "requirement", not "requirements")
- **.env.example**: Template for environment variables
- **.env**: Actual credentials (created by user, not in repo)

### Core Functionality
- **Date Logic**: Processes previous month's data (current month - 1)
- **Weekday Detection**: Different step counts for weekdays (8000) vs weekends (15000)
- **Random Variation**: Adds 0-1000 random steps to make data appear natural
- **Form Automation**: Fills walking steps, sleep hours, and checkboxes automatically
- **Error Handling**: Graceful handling of WebDriver version mismatches

### Dependencies
Key libraries (all specified in requirement.txt):
- selenium==4.34.2 (WebDriver automation)
- python-dotenv==1.0.1 (Environment variable loading)
- All other dependencies are selenium sub-dependencies

## Common Issues and Solutions

### Network and Connectivity Issues
**pip install timeout**: In restricted network environments, pip may timeout downloading packages
**Solution**: Install packages individually or use offline installation methods

**WebDriver connectivity**: Application requires internet access to navigate to pepup.life
**Solution**: Ensure stable internet connection before running automation

### WebDriver Version Mismatch
**Error**: "This version of Microsoft Edge WebDriver only supports Microsoft Edge version XXX"
**Solution**: Download matching WebDriver version from Microsoft's site

### Missing .env File
**Error**: "Email and Password must be set in .env file"
**Solution**: Copy .env.example to .env and add real credentials

### reCAPTCHA Timeout
**Behavior**: Application waits 30 seconds for manual reCAPTCHA solving
**Solution**: Solve reCAPTCHA within 30 seconds when browser opens

### No Input Elements Found
**Behavior**: "No inputs found" message and early termination
**Cause**: Either wrong date format or pepup.life page structure changed
**Solution**: Check target URL format and page structure

## Development Guidelines

### Making Changes
- Always activate virtual environment before any operations
- Test utility functions first (they don't require WebDriver)
- Use webdriver-manager for development to avoid manual WebDriver setup
- Never commit .env file or WebDriver executables
- Run linting checks before committing

### Testing Without Browser
Most functionality can be tested without WebDriver:
- Date calculations (funcs.py)
- Configuration loading (config.py)  
- Import validation
- Syntax checking

### Timing Expectations
- Virtual environment creation: ~3 seconds
- Dependency installation: ~15-30 seconds (may timeout in restricted networks)
- Application startup: ~5 seconds
- Full month processing: 5-10 minutes (depends on days in month)
- Syntax checking: <0.1 seconds
- Linting (flake8): ~0.1 seconds
- Format checking (black): ~0.2 seconds

**NEVER CANCEL long-running operations. Always set appropriate timeouts.**

## NO TESTS
This repository does not include automated tests. All validation must be done manually using the scenarios described above.

## NO CI/CD
This repository does not have automated CI/CD pipelines. All quality checks must be run manually before committing changes.