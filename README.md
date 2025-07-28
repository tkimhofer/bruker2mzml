[![Docker Image CI](https://github.com/tkimhofer/bruker2mzml/actions/workflows/docker-image.yml/badge.svg)](https://github.com/tkimhofer/bruker2mzml/actions/workflows/docker-image.yml)

# Bruker2mzML Converter

**Bruker2mzML** is a cross-platform command-line tool for converting Bruker mass spectrometry `.d` folders into open formats like `.mzML`.  
It wraps the Bruker `baftosql` tool inside a Linux-based Docker container, making it easy to use on **Windows**, **macOS**, and **Linux** — without any software installs or manual configuration.

---

## 🔧 Features

- ✅ Converts Bruker `.d` directories to `.mzML` format
- 🐧 Built on a lightweight Linux container
- 💻 Runs on Windows, macOS, and Linux (via Docker)
- 🔁 Simple CLI interface for batch or single-file processing

---

## 📦 Requirements

- Docker (Windows/macOS/Linux)
- A Bruker `.d` folder as input

---

## 🚀 Quick Start

### 1. Install Docker
- [Download Docker Desktop](https://www.docker.com/products/docker-desktop) and follow installation steps for your platform.

### 2. Clone this repository
```bash
git clone https://github.com/tkimhofer/bruker2mzml.git
cd bruker2mzml
```

### 3. Build the Docker image
```bash
docker build -t bruker2mzml .
```

### 4. Run the converter
Place your Bruker `.d` folder into a directory (e.g. `~/bruker-data`), then run:

```bash
docker run --rm -v ~/bruker-data:/data bruker2mzml /data/sample.d
```

> Output will be written to the same folder.

---

## 🔗 LIMS Integration

`bruker2mzml` is well-suited for automated workflows that feed mass spectrometry data into a Laboratory Information Management System (LIMS). By converting Bruker `.d` folders into standardized `.mzML` files, the tool simplifies downstream integration, reduces data size, and ensures compatibility with open formats preferred by LIMS platforms. Its Docker-based design makes it easy to deploy on acquisition servers, enabling hands-free conversion and data submission immediately after acquisition — ideal for fully automated pipelines in regulated or high-throughput environments.

---

## 👩‍🔬 Who Is This For?

This tool is ideal for:
- Lab technicians
- Mass spec analysts
- Anyone needing a quick, reliable way to extract open-format data from Bruker files — **without needing to install complicated software or scripts**.

---

## 📝 License

MIT License

---

## 🤝 Acknowledgements

- Bruker `baftosql` tool
- Docker
- Python & R mass spectrometry communities
