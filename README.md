# Intelligence-to-Deck: AI-Powered Presentation Generation

Convert any document into professional presentations using AI. Choose between two optimized workflows:

## 🚀 Quick Start

### Option 1: Python-Decktopus Workflow (v1)

**Best for:** Marp/PDF output → Decktopus import

```bash
# Generate Marp slides for Decktopus
python src/v1/full_workflow.py input.txt --type business --format marp --theme uncover
```

### Option 2: Python-Slides Workflow (v2)

**Best for:** Native Google Slides collaboration

```bash
# Generate Google Slides presentation
python src/v2/full_workflow.py input.txt --type business --format slides --title "My Presentation"
```

## 📁 Project Structure

```
├── inputs/                     # Place your source documents here
├── outputs/                    # Generated presentations appear here
├── credentials.json            # Google Slides API credentials (for v2)
├── src/
│   ├── v1/                    # Python-Decktopus Workflow
│   │   ├── full_workflow.py   # Complete automation
│   │   ├── prepare_content.py # Text preprocessing
│   │   ├── generate_slides.py # AI slide generation
│   │   └── readme.md          # Detailed v1 documentation
│   ├── v2/                    # Python-Slides Workflow
│   │   ├── full_workflow.py   # Complete automation
│   │   ├── prepare_content.py # Text preprocessing
│   │   ├── generate_slides.py # AI slide generation
│   │   ├── example_google_slides_workflow.py
│   │   └── readme.md          # Detailed v2 documentation
│   └── utils/                 # Shared utilities
│       ├── smart_chunk.py     # Advanced document chunking
│       └── exporters/
│           ├── marp_generator.py    # Marp markdown export
│           ├── google_slides.py     # Google Slides API
│           └── README_Google_Slides.md
```

## 🔄 Workflow Comparison

| Feature              | Python-Decktopus (v1) | Python-Slides (v2)   |
| -------------------- | --------------------- | -------------------- |
| **Primary Output**   | Marp Markdown → PDF   | Native Google Slides |
| **Best For**         | Decktopus import      | Team collaboration   |
| **Collaboration**    | PDF sharing           | Real-time editing    |
| **Setup Complexity** | Simple                | Requires Google API  |
| **Editability**      | Limited (Markdown)    | Full visual editing  |

## 🛠️ Setup

### Basic Setup (Both Workflows)

```bash
# Install Python dependencies
pip install openai

# Set OpenAI API key
export OPENAI_API_KEY="your-api-key-here"

# Create directories
mkdir -p inputs outputs
```

### Additional Setup for Python-Slides (v2)

```bash
# Install Google API dependencies
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib

# Set up Google Slides API credentials
# 1. Go to https://console.cloud.google.com/
# 2. Enable Google Slides API
# 3. Create OAuth 2.0 credentials
# 4. Download credentials.json to project root
```

### Optional: Marp CLI (for PDF generation)

```bash
npm install -g @marp-team/marp-cli
```

## 📋 Workflow Commands

### Python-Decktopus Workflow (v1)

```bash
# Complete workflow - generate Marp slides
python src/v1/full_workflow.py script_1.txt --type business --format marp

# Individual steps
python src/v1/prepare_content.py script_1.txt cleaned.txt
python src/v1/generate_slides.py script_1.txt --type business
python src/utils/exporters/marp_generator.py outputs/script_1_slides.txt outputs/slides.md

# Generate PDF
marp outputs/slides.md -o outputs/presentation.pdf
```

### Python-Slides Workflow (v2)

```bash
# Complete workflow - generate Google Slides
python src/v2/full_workflow.py script_1.txt --type business --format slides --title "Business Plan"

# Test setup with example
python src/v2/example_google_slides_workflow.py

# Individual steps
python src/v2/prepare_content.py script_1.txt cleaned.txt
python src/v2/generate_slides.py script_1.txt --type business
python src/utils/exporters/google_slides.py outputs/script_1_comprehensive_script.txt "My Presentation"
```

## 🎯 Content Types

Both workflows support:

- `business`: Problem → Analysis → Solution → ROI
- `technical`: Architecture → Analysis → Implementation
- `sales`: Pain → Solution → Proof → ROI

## 💰 Cost Estimation

```bash
# See estimated costs before running
python src/v1/generate_slides.py input.txt --dry-run
python src/v2/generate_slides.py input.txt --dry-run
```

Typical costs:

- Short document (2K words): ~$0.15
- Medium document (10K words): ~$0.75
- Large document (20K words): ~$1.50
- Google Slides API: Free (generous quotas)

## 🔧 Advanced Features

### Smart Document Chunking

```bash
# Handle large documents automatically
python src/utils/smart_chunk.py large_document.txt --strategy sections --format json
```

### Custom Themes (Marp)

```bash
# Use different Marp themes
python src/v1/full_workflow.py input.txt --format marp --theme gaia
python src/v1/full_workflow.py input.txt --format marp --theme uncover
```

### Multiple Output Formats

```bash
# JSON output for custom processing
python src/v1/full_workflow.py input.txt --format json
python src/v2/full_workflow.py input.txt --format json

# Plain text slides
python src/v1/full_workflow.py input.txt --format txt
python src/v2/full_workflow.py input.txt --format txt
```

## 📖 Detailed Documentation

- **[Python-Decktopus Workflow](src/v1/readme.md)** - Complete v1 documentation
- **[Python-Slides Workflow](src/v2/readme.md)** - Complete v2 documentation
- **[Google Slides Setup Guide](src/utils/exporters/README_Google_Slides.md)** - API setup instructions

## 🚦 Getting Started

1. **Choose your workflow** based on your needs
2. **Follow the setup** instructions above
3. **Place your document** in the `inputs/` folder
4. **Run the appropriate command** for your chosen workflow
5. **Find your presentation** in the `outputs/` folder

## 🤝 Use Cases

### Choose Python-Decktopus (v1) if you:

- Want to import PDFs into Decktopus for styling
- Prefer markdown-based workflows
- Need simple, fast setup
- Want to create PDFs for sharing

### Choose Python-Slides (v2) if you:

- Need real-time collaboration
- Want native Google Slides features
- Work with teams regularly
- Prefer visual editing interfaces

## 🔄 Migration

Both workflows share the same core AI generation, so you can easily switch between them or use both for different purposes.

## ⚡ Quick Examples

```bash
# Quick Decktopus workflow
python src/v1/full_workflow.py inputs/meeting_notes.txt --type business --format marp

# Quick Google Slides workflow
python src/v2/full_workflow.py inputs/meeting_notes.txt --type business --format slides --title "Meeting Summary"
```

Your presentations will be ready in the `outputs/` folder!
