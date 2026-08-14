<div align="center">
# 🚀 Pathfinder Aviation Manual Orchestrator
### *Modern, High-Performance Python Solution & Developer Suite*

<p align="center">
  [![Architect](https://img.shields.io/badge/Architect-Hsini%20Mohamed-0055ff?style=for-the-badge&logo=github&logoColor=white)](https://hsini.dev)
  [![Portfolio](https://img.shields.io/badge/Portfolio-hsini.dev-00c853?style=for-the-badge&logo=google-chrome&logoColor=white)](https://hsini.dev)
  [![Language](https://img.shields.io/badge/Language-Python-3776AB?style=for-the-badge)](https://github.com/hsinidev)
  [![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
</p>

</div>

---
## 🌟 Executive Overview

**Pathfinder Aviation Manual Orchestrator** is a production-grade **Python** platform engineered for high reliability, clean architectural separation, and frictionless developer workflow.

## ⚡ Key Highlights & Capabilities

- **Scalable Architecture**: Modular, decoupled components adhering to clean code principles.
- **Optimized Runtime**: Ultra-fast execution with minimal memory and CPU overhead.
- **Developer Tooling**: Standardized linting, formatting, and rapid local iteration setup.
- **Production Ready**: Built-in error resilience, validation, and structured logging.

---
## 🏗️ Architecture & Technology Stack

- **Primary Language**: `Python`
- **Design Pattern**: Modular Clean Architecture / Domain-Driven Design
- **License**: MIT Open Source Attribution

## 📖 Deep-Dive Technical Documentation

# PATHFINDER - Aviation Maintenance & Flight Manual Orchestrator


## 🎯 Project Overview
**PATHFINDER** is an air-gapped, high-reliability Retrieval-Augmented Generation (RAG) system engineered for aircraft maintenance technicians, flight engineers, and aviation mechanics. Designed to operate inside metal hangars, remote runways, and un-networked environments, PATHFINDER provides instant retrieval of Flight Crew Operating Manuals (FCOM), maintenance repair bulletins, and cockpit troubleshooting guides.

---

## ✨ Key Features
- ✈️ **Aviation Manual Search**: Instant page and section matching across complex airliner systems (hydraulic, avionics, flight control, engine specs).
- 🎛️ **Visual Cockpit Assistance**: Ingests cockpit instrument photos and indicator lights to identify error codes and system alert states.
- 📶 **100% Hangar & Tarmac Offline Reliability**: Self-contained vector database and local LLM runtime requiring zero cellular or internet access.
- 🛠️ **Service Bulletin Cross-Referencing**: Links mechanical fault symptoms to official manufacturer service bulletins and repair procedures.
- ⚡ **High-Precision Technical Extraction**: Accurately extracts torque settings, part numbers, and safety clearances.

---

## 🛠 System Architecture & Stack
- **Interface**: Custom Aviation Engineering Dashboard (`app.py`)
- **RAG Engine**: High-reliability aviation retrieval engine (`rag_engine.py`) using ChromaDB
- **Data Ingestion**: Multi-page PDF flight manual & repair bulletin indexer (`ingest.py`)
- **LLM Runtime**: Local Ollama execution (Llama 3 / LLaVA / Gemma 2)

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.10+
- [Ollama](https://ollama.ai/) installed locally

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/hsinidev/PATHFINDER_Aviation_Manual_Orchestrator.git
   cd PATHFINDER_Aviation_Manual_Orchestrator
   ```
2. Activate a Python virtual environment:
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux/macOS:
   source venv/bin/activate
   ```
3. Install required packages:
   ```bash
   pip install streamlit chromadb langchain ollama pypdf pillow
   ```

### Usage
1. Place aircraft flight manuals, maintenance manuals, and repair bulletins in the local data directory.
2. Index aviation documentation:
   ```bash
   python ingest.py
   ```
3. Start the PATHFINDER aviation maintenance console:
   ```bash
   streamlit run app.py
   ```

---

## 📂 Project Structure
```
PATHFINDER_Aviation_Manual_Orchestrator/
├── app.py           # Aircraft maintenance console & query interface
├── ingest.py        # Aviation manual PDF parser & vector embedding script
├── rag_engine.py    # High-precision technical retrieval engine
├── prompt.json      # Aviation engineer prompts & fault resolution models
├── system.txt       # System role definition & flight safety policy
├── skills.md        # Specialized aviation maintenance tool definitions
└── README.md        # Project documentation
```

---

**HSINI MOHAMED**  
*Enterprise Systems Architect & Aviation Systems Engineer*  

- **GitHub**: [@hsinidev](https://github.com/hsinidev)
- **LinkedIn**: [Moahmed Hsini](https://www.linkedin.com/in/moahmed-hsini-6059281a1/)
- **Email**: [hsini.moahmed@gmail.com](mailto:hsini.moahmed@gmail.com)
- **Website**: [hsini.dev](https://hsini.dev)

---
*Precision flight safety and offline aviation technical manual intelligence.*

---
## 🚀 Quick Start & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/hsinidev/PATHFINDER_Aviation_Manual_Orchestrator.git
cd PATHFINDER_Aviation_Manual_Orchestrator
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch the Application
```bash
python main.py
```


---

## 👨‍💻 System Architect & Author

<table align="center" style="border: none; background: transparent; width: 100%;">
  <tr>
    <td align="center" width="160" style="border: none; padding: 12px;">
      <img src="https://avatars.githubusercontent.com/u/232697467?v=4" width="120" height="120" style="border-radius: 50%; box-shadow: 0 8px 24px rgba(99,102,241,0.3); border: 2.5px solid #6366f1;" alt="Hsini Mohamed" />
      <br /><br />
      <b>Hsini Mohamed</b><br />
      <sub>Morocco 🇲🇦</sub>
    </td>
    <td style="border: none; padding: 12px; vertical-align: middle;">
      <h3 style="margin-top: 0;">🚀 System Architect & Full-Stack Engineer</h3>
      <p style="font-size: 0.95rem; line-height: 1.6; color: #475569;">
        Specializing in high-performance autonomous AI systems, deterministic multi-agent swarms, enterprise cloud architecture, and modern full-stack engineering.
      </p>
      <p>
        <a href="https://hsini.dev"><img src="https://img.shields.io/badge/Portfolio-hsini.dev-2563eb?style=flat-square&logo=google-chrome&logoColor=white" alt="Portfolio" /></a>
        <a href="mailto:contact@hsini.dev"><img src="https://img.shields.io/badge/Email-contact@hsini.dev-ea4335?style=flat-square&logo=gmail&logoColor=white" alt="Email" /></a>
        <a href="https://github.com/hsinidev"><img src="https://img.shields.io/badge/GitHub-@hsinidev-181717?style=flat-square&logo=github&logoColor=white" alt="GitHub" /></a>
        <a href="https://linkedin.com/in/hsinidev/"><img src="https://img.shields.io/badge/LinkedIn-hsinidev-0077b5?style=flat-square&logo=linkedin&logoColor=white" alt="LinkedIn" /></a>
      </p>
    </td>
  </tr>
</table>

---

## 📄 License & Attribution

This project is distributed under the **MIT License**. See [`LICENSE`](LICENSE) for complete terms.

<div align="center">
  <sub>⚡ Designed, architected, and maintained with engineering precision by <b><a href="https://hsini.dev">Hsini Mohamed</a></b>.</sub>
</div>
