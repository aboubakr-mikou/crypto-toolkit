
<h1 align="center">CryptoToolkit 1.0</h1>

<p align="center">
  <b>Offline Cryptography & Cybersecurity Workbench</b>
</p>

<p align="center">
  <a href="https://github.com/aboubakr-mikou/crypto-toolkit/actions/workflows/tests.yml">
    <img src="https://github.com/aboubakr-mikou/crypto-toolkit/actions/workflows/tests.yml/badge.svg" alt="Tests"/>
  </a>
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-0078D4" alt="Platform"/>
  <img src="https://img.shields.io/badge/Mode-Offline-success" alt="Offline"/>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="MIT License"/>
  </a>
  <img src="https://img.shields.io/badge/Release-v1.0.0-159B83" alt="Version"/>
</p>

---

## Overview

CryptoToolkit is a Python-based desktop application designed for cryptography, educational purposes, and authorized cybersecurity assessments.

Originally developed as an academic cryptography project at ENSA Fès, it has been redesigned into a modern security workbench offering practical cryptographic utilities through a dark-themed graphical interface.

The application operates entirely offline. All cryptographic operations and data processing are performed locally, without external requests or telemetry.

## Download

<p align="center">
  <a href="https://github.com/aboubakr-mikou/crypto-toolkit/releases/download/v1.0.0/CryptoToolkit.exe">
    <img src="https://img.shields.io/badge/Download_for_Windows-238636?style=for-the-badge&logo=windows&logoColor=white" alt="Download CryptoToolkit for Windows"/>
  </a>
</p>

<p align="center">
  <b>Windows x64 | No Python required | v1.0.0</b>
</p>

<p align="center">
  <a href="https://github.com/aboubakr-mikou/crypto-toolkit/releases">All Releases</a>
  |
  <a href="https://github.com/aboubakr-mikou/crypto-toolkit/releases/download/v1.0.0/SHA256SUMS.txt">SHA-256 Checksum</a>
</p>

### Verify Download Integrity

To verify the integrity of the downloaded executable, run the following command in PowerShell:

```powershell
Get-FileHash .\CryptoToolkit.exe -Algorithm SHA256
```

Compare the resulting hash with the value provided in `SHA256SUMS.txt`.

The executable is not digitally signed and may trigger a Windows SmartScreen warning. A matching checksum verifies consistency with the published checksum, not the identity of the publisher.

---

## Screenshots

### Security Dashboard

![Security Dashboard](docs/screenshots/dashboard.png)

### AES Encryption Workspace

![AES Workspace](docs/screenshots/aes.png)

*Screenshots captured on Linux. Appearance may vary slightly on Windows.*

---

## Features

| Module | Capabilities |
| --- | --- |
| AES Encryption | AES-256-GCM authenticated encryption and decryption, random key generation, Base64 ciphertext |
| RSA Toolkit | RSA-2048 key generation, OAEP encryption and decryption with SHA-256 |
| Hash Analyzer | Text and file hashing, SHA-256, SHA-512, MD5 and SHA-1, integrity comparison |
| Digital Signatures | RSA-PSS signature generation and verification |
| Certificate Inspector | X.509 PEM/DER inspection, self-signed laboratory certificates and encrypted private key export |
| Encoder | Base64 and hexadecimal encoding and decoding, HMAC-SHA256 |
| Secret Generator | Cryptographically secure random secret and token generation |

### Additional Features

- Modern dark-themed graphical interface
- Offline and local processing
- Import and export utilities
- Clipboard integration
- Persistent workspace data during navigation
- Automated cryptographic and GUI tests
- Continuous integration with GitHub Actions
- Standalone Windows executable

---

## Tech Stack

### Programming & Interface

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/Tkinter-34495E?style=for-the-badge)

### Cryptography

![Cryptography](https://img.shields.io/badge/Cryptography-159B83?style=for-the-badge)
![AES](https://img.shields.io/badge/AES--256--GCM-34495E?style=for-the-badge)
![RSA](https://img.shields.io/badge/RSA--2048-34495E?style=for-the-badge)
![SHA](https://img.shields.io/badge/SHA--256-34495E?style=for-the-badge)

### Development & Automation

![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)
![PyInstaller](https://img.shields.io/badge/PyInstaller-34495E?style=for-the-badge)

---

## Installation from Source

### Prerequisites

- Python 3.10 or later
- Tkinter
- Git (optional when downloading the source ZIP)

### Clone the Repository

```bash
git clone https://github.com/aboubakr-mikou/crypto-toolkit.git
cd crypto-toolkit
```

Alternatively, download the source code using **Code → Download ZIP** and extract the archive.

### Windows — PowerShell

Create a virtual environment:

```powershell
py -m venv .venv
```

Install dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Launch the application:

```powershell
.\.venv\Scripts\python.exe main.py
```

### Linux — Debian / Ubuntu

Install the required system packages if necessary:

```bash
sudo apt update
sudo apt install python3-tk python3-venv
```

Create the virtual environment and install dependencies:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

Launch the application:

```bash
.venv/bin/python main.py
```

Compatibility with macOS has not been verified.

### Quick Start — Windows

After downloading or cloning the source code, double-click:

```text
launch.bat
```

The launcher creates a virtual environment, installs dependencies on first use, and starts CryptoToolkit.

Python and an internet connection are required for the initial setup.

---

## Usage

1. Launch CryptoToolkit.
2. Select a security module from the sidebar.
3. Generate or provide the required cryptographic key when applicable.
4. Enter or import the data to process.
5. Execute the desired operation.
6. Copy or export the result when necessary.

### Key and Data Management

- RSA and signing session keys are stored in memory and lost when the application closes.
- Store AES keys securely if you need to decrypt data later.
- Workspace data remains in memory while navigating between modules.
- Clear sensitive inputs and close the application after use.
- Text imports are limited to 2 MiB.
- Exported files may contain sensitive information.
- File hashes should be compared against trusted reference values.

---

## Project Architecture

```text
crypto-toolkit/
├── .github/
│   └── workflows/
│       └── tests.yml
├── core/
│   ├── __init__.py
│   ├── asymmetric.py
│   ├── certificate.py
│   ├── hashing.py
│   ├── signature.py
│   ├── symmetric.py
│   └── toolkit.py
├── gui/
│   ├── __init__.py
│   └── main_window.py
├── docs/
│   └── screenshots/
│       ├── dashboard.png
│       └── aes.png
├── tests/
│   ├── legacy_demo.py
│   ├── test_gui.py
│   └── test_toolkit.py
├── .gitignore
├── LICENSE
├── README.md
├── launch.bat
├── main.py
└── requirements.txt
```

The project separates cryptographic operations, graphical components, documentation, and automated tests to improve maintainability.

| Component | Responsibility |
| --- | --- |
| `core/` | Cryptographic operations and security utilities |
| `gui/` | Graphical interface and user interaction |
| `tests/` | Automated tests and original demonstration script |
| `docs/` | Application documentation and screenshots |
| `.github/` | Continuous integration workflow |
| `main.py` | Application entry point |

---

## Testing & Continuous Integration

CryptoToolkit includes automated tests for its cryptographic operations and graphical interface.

Run the test suite from an environment with the project dependencies installed:

```bash
python -m unittest discover -s tests -v
```

On Linux, GUI tests can be executed using a virtual display:

```bash
xvfb-run -a python -m unittest discover -s tests -v
```

GitHub Actions automatically runs the configured test suite on pushes and pull requests.

[View CI Workflow](https://github.com/aboubakr-mikou/crypto-toolkit/actions/workflows/tests.yml)

---

## Security Considerations

CryptoToolkit is an educational security utility and has not undergone an independent security audit. It is not intended for production key management.

- AES-GCM uses fresh random nonces and authenticated encryption.
- AES ciphertext follows the toolkit's own format: nonce, ciphertext and authentication tag, Base64 encoded, with fixed associated data.
- RSA encryption uses OAEP with SHA-256.
- Digital signatures use RSA-PSS.
- MD5 and SHA-1 are provided for legacy comparison only.
- Self-signed certificates are intended for laboratory use.
- Certificate inspection does not validate trust chains or hostnames.
- Legacy AES-CBC and unencrypted private key export methods remain in the original core modules for educational reference, but are not exposed through the redesigned GUI.
- Clipboard contents and exported files may expose sensitive information.
- Never commit private keys, passwords or real secrets to a repository.

Use this toolkit responsibly and only within authorized environments.

---

## License

This project is distributed under the MIT License.

See the [LICENSE](LICENSE) file for more information.

---

## Author

**Aboubakr Mikou**

Computer Science Engineering Student at ENSA Fès.

Interests: Cybersecurity, Artificial Intelligence, Cloud Computing and DevOps.

<p>
  <a href="https://github.com/aboubakr-mikou">
    <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"/>
  </a>
  <a href="https://www.linkedin.com/in/aboubakr-mikou-8441bb381">
    <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge" alt="LinkedIn"/>
  </a>
  <a href="mailto:aboubakrmikou2411@gmail.com">
    <img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Email"/>
  </a>
</p>

---

<p align="center">
  <i>Built for learning, experimentation, and responsible cybersecurity.</i>
</p>
