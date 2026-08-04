# PATHFINDER - Aviation Maintenance & Flight Manual Orchestrator

![PATHFINDER Banner](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge&logo=plane)
![Aviation](https://img.shields.io/badge/Aviation-Air--Gapped%20Hangar%20Ready-blue?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-orange?style=for-the-badge)

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

## 👤 Author & Maintainer
**HSINI MOHAMED**  
*Enterprise Systems Architect & Aviation Systems Engineer*  

- **GitHub**: [@hsinidev](https://github.com/hsinidev)
- **LinkedIn**: [Moahmed Hsini](https://www.linkedin.com/in/moahmed-hsini-6059281a1/)
- **Email**: [hsini.moahmed@gmail.com](mailto:hsini.moahmed@gmail.com)
- **Website**: [hsini.dev](https://hsini.dev)

---
*Precision flight safety and offline aviation technical manual intelligence.*
