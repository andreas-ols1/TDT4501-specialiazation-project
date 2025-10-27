# TSMini Experiment

This repository contains the experimental setup for testing and evaluating the **TSMini** model on trajectory similarity tasks.  
It builds upon the [TSMini](https://github.com/changyanchuan/TSMini) architecture and provides an example inference script for running experiments.

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/andreas-ols1/TDT4501-specialiazation-project.git
cd TDT4501-specialiazation-project/TSMini_Experiment
```

If you are on Windows, it is recommended to use WSL (Ubuntu) for running the code.

### 2. Create and activate a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
'''bash
pip install -r requirements.txt
'''

### 4. Run inference
'''bash
cd code
python3 infer_tsmini.py
'''