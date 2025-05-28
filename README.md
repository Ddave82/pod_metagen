# POD Metadata Generator

A local tool to automate the generation of SEO-optimized metadata for Print-on-Demand platforms like TeePublic, Redbubble, Spreadshirt, and Amazon Merch – powered by GPT-4o Vision and Streamlit.

![Demo](assets/demo.gif)

## Features

- 📤 Upload a design image from your computer
- 🤖 Automatic image analysis with GPT-4o Vision
- 📝 Platform-specific SEO metadata generation
- 🌐 Multi-platform support in one step
- 🧠 Local Streamlit interface in the browser


## Screenshots

### 1. Upload eines Bildes
![Upload Screenshot](assets/screenshot-1.png)

### 2. Auswahl der Plattformen
![Platform Selection Screenshot](assets/screenshot-2.png)

### 3. Generierte Metadaten
![Generated Metadata Screenshot](assets/screenshot-3.png)



## Language Note

This tool is currently preconfigured to generate:

- **German** metadata for:
  - Spreadshirt
  - Amazon Merch

- **English** metadata for:
  - TeePublic

This is because the author is based in Germany and uses those platforms locally.

If you want to generate metadata in **English** (or another language), simply open the file `app.py` and look for the **prompt templates** in the `generate_metadata()` function. You can adjust the wording or language there to suit your needs.

## Requirements

- Python 3.11+
- OpenAI API key (not included in the repo)
- Internet access (to connect to the OpenAI API)

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

Once started, the app will be available in your browser at:  
👉 http://localhost:8501

## .env Configuration

Create a file named `.env` in the root of the project and add your OpenAI API key:

```
OPENAI_API_KEY=sk-...
```

🚫 Never share this key.  
✅ `.env` is excluded via `.gitignore`.

You’ll also find an example file here:
```
.env.example
```

## File Structure

```
pod_metagen/
├── app.py                # Main app logic with prompts
├── requirements.txt      # Python dependencies
├── README.md             # This file
├── .gitignore            # Exclude env and build files
├── .env.example          # Example environment file
└── assets/
    └── demo.gif          # Optional: Visual demo of the tool
```

## Supported Platforms & Metadata Rules

| Platform       | Language | Metadata Rules                                                                 |
|----------------|----------|---------------------------------------------------------------------------------|
| TeePublic      | English  | Title (max 8 words), Description (max 300 chars), Main Tag, 8 Tags             |
| Redbubble      | German   | Title (max 8 words), Description (max 300 chars), exactly 15 Tags              |
| Spreadshirt    | German   | Title (max 50 chars), Description (max 200 chars), up to 25 Tags              |
| Amazon Merch   | German   | Title (max 60 chars), Brand (max 50 chars), 2 Bullet Points, Product Text     |

## License

[GPL-3.0 License](LICENSE)

---

Built with ❤️ to simplify your Print-on-Demand workflow using AI and automation.
