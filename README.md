# POD Metadata Generator

A local tool to automate the generation of SEO-optimized metadata for Print-on-Demand platforms like TeePublic, Redbubble, Spreadshirt, and Amazon Merch – powered by GPT-4o Vision and Streamlit.

## Features
- Upload a design image from your computer
- Automatic image analysis with GPT-4o Vision
- Platform-specific SEO metadata generation
- Support for multiple platforms simultaneously
- Clean and modern Streamlit interface (runs in the browser)

## Requirements
- Python 3.11 or higher
- An OpenAI API key (not included in the repository)
- Internet connection (for API access)

## Installation

```bash
git clone https://github.com/your-username/pod_metagen.git
cd pod_metagen
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run the App

```bash
streamlit run app.py
```

The app will open in your default browser at [http://localhost:8501](http://localhost:8501).

## .env Configuration

Create a `.env` file in the root directory with the following content:

```
OPENAI_API_KEY=sk-...
```

Make sure your API key remains private.  
`.env` and the `venv/` folder are excluded from Git via `.gitignore`.

## Supported Platforms

| Platform       | Language | Metadata Types                                 |
|----------------|----------|------------------------------------------------|
| TeePublic      | English  | Title (max 8 words), Description (max 300 chars), Main Tag, 8 Tags |
| Redbubble      | German   | Title (max 8 words), Description (max 300 chars), exactly 15 Tags |
| Spreadshirt    | German   | Title (max 50 chars), Description (max 200 chars), up to 25 Tags |
| Amazon Merch   | German   | Title (max 60 chars), Brand (max 50 chars), 2 Bullet Points (256 chars each), Product Description (max 1900 chars) – **no use of "T-Shirt" or "Shirt" allowed** |

## File Structure

```
pod_metagen/
├── app.py              # Main Streamlit app
├── .env                # Your OpenAI API key (excluded from Git)
├── requirements.txt    # Python dependencies
├── README.md           # This file
├── .gitignore          # Excludes .env and venv from Git
└── venv/               # Virtual environment (excluded from Git)
```

---

Built with ❤️ to simplify your Print-on-Demand workflow using the power of AI.
