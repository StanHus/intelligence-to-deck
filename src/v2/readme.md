# Intelligence-to-Deck Python Scripts (v2)

## Python-Slides Workflow

**This is the enhanced workflow with Google Slides API integration.**

Python utilities for converting documents to presentation slides via AI workflows with native Google Slides output.

## Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Or install individual packages
pip install openai google-api-python-client google-auth-httplib2 google-auth-oauthlib

# Install Marp CLI (optional, for Marp format)
npm install -g @marp-team/marp-cli

# Set API keys
export OPENAI_API_KEY="your-api-key-here"

# For Google Slides generation
# 1. Enable Google Slides API in Google Cloud Console
# 2. Download credentials.json file
# 3. Place credentials.json in project root
```

## Usage

### Complete Workflow (Python-Slides)

```bash
# Google Slides generation via Google Slides API (recommended)
python src/v2/full_workflow.py input.txt --type business --format slides --title "Business Plan"

# Text output
python src/v2/full_workflow.py input.txt --type business --format txt

# Marp markdown slides
python src/v2/full_workflow.py input.txt --type business --format marp --theme uncover
```

### Individual Components

```bash
# Text preprocessing
python src/v2/prepare_content.py input.txt clean.txt

# Slide generation (15-20 slides)
python src/v2/generate_slides.py clean.txt --type business

# Google Slides generation
python src/utils/exporters/google_slides.py slides.txt "Presentation Title"

# Marp conversion
python src/utils/exporters/marp_generator.py slides.txt presentation.md
```

## Options

**Content Types**: `business`, `technical`, `general`  
**Output Formats**: `txt`, `marp`, `json`, `slides`  
**Models**: `gpt-4-turbo` (default), `gpt-4`

## File Structure

```
├── inputs/                     # Source documents
├── outputs/                    # Generated presentations
├── credentials.json            # Google Slides API credentials
├── src/
│   └── v2/                    # Python-Slides workflow
│       ├── full_workflow.py   # Complete automation
│       ├── prepare_content.py # Text preprocessing
│       ├── generate_slides.py # AI slide generation
│       ├── example_google_slides_workflow.py # Example demo
│       └── readme.md          # This file
│   └── utils/
│       └── exporters/
│           ├── marp_generator.py  # Marp markdown export
│           └── google_slides.py   # Google Slides API integration
```

## Complete Automated Workflow

```bash
# One command to rule them all - Python-Slides
python src/v2/full_workflow.py script_1.txt --format slides

# Or with options
python src/v2/full_workflow.py script_1.txt --type business --format slides --title "Strategic Plan 2024"

# Alternative formats
python src/v2/full_workflow.py script_1.txt --type business --format marp --theme uncover
```

This runs the entire pipeline:

1. **Prepare**: Clean and chunk content
2. **Generate**: Create slides with OpenAI
3. **Convert**: Transform to desired format
4. **Export**: Generate final output (Google Slides, PDF, etc.)

## Google Slides Integration

### Google Slides API Integration

The system integrates with [Google Slides API](https://developers.google.com/slides/api) for professional presentation generation with full collaboration features.

**Features:**

- Native Google Slides output
- Real-time collaboration
- Cloud-based accessibility
- Professional formatting
- Shareable presentations

**Setup:**

1. Enable Google Slides API in [Google Cloud Console](https://console.cloud.google.com/)
2. Create OAuth 2.0 credentials for desktop application
3. Download `credentials.json` file to project root
4. Use `--format slides` option

**Example:**

```bash
# Generate Google Slides presentation
python src/v2/full_workflow.py content.txt --format slides --title "Business Strategy"

# Result: Shareable Google Slides presentation link
```

### Example Demo

Run the included example to test your setup:

```bash
python src/v2/example_google_slides_workflow.py
```

See [Google Slides README](../utils/exporters/README_Google_Slides.md) for detailed setup instructions.

## Individual Scripts

### Text Preprocessing

```bash
python src/v2/prepare_content.py input.txt [output.txt]
```

### AI Slide Generation

```bash
python src/v2/generate_slides.py prepared.txt --type business --model gpt-4-turbo
```

### Google Slides Generation

```bash
python src/utils/exporters/google_slides.py slides.txt "Presentation Title"
```

### Marp Conversion

```bash
python src/utils/exporters/marp_generator.py slides.txt presentation.md uncover
marp presentation.md -o final.pdf
```

### Advanced Chunking

```bash
python src/utils/smart_chunk.py input.txt --strategy sections --format json
```

## Workflow Options

**Presentation Types**:

- `business`: Problem → Analysis → Solution → ROI
- `technical`: Architecture → Analysis → Implementation
- `sales`: Pain → Solution → Proof → ROI

**Output Formats**:

- `slides`: Native Google Slides via Google Slides API (recommended)
- `txt`: Plain text slides
- `marp`: Automated markdown → PDF generation
- `json`: Structured slide data

**Models**:

- `gpt-4-turbo`: Best quality, moderate cost
- `gpt-4`: Highest quality, higher cost
- `gpt-3.5-turbo`: Fast and cheap

## Cost Estimation

```bash
# See cost before running
python src/v2/generate_slides.py input.txt --dry-run
```

Typical costs:

- Short transcript (2K words): ~$0.15
- Long document (10K words): ~$0.75
- Research report (20K words): ~$1.50
- Google Slides API: Free (subject to quotas)

## Example with script_1.txt

```bash
# Complete automation - Python-Slides workflow
python src/v2/full_workflow.py script_1.txt --type business --format slides --title "Business Plan"

# Text output
python src/v2/full_workflow.py script_1.txt --type business

# Manual steps
python src/v2/prepare_content.py script_1.txt clean.txt
python src/v2/generate_slides.py clean.txt --type business
python src/utils/exporters/google_slides.py clean_slides.txt "Business Presentation"
```

## Requirements

- Python 3.7+
- OpenAI API key
- Google Cloud project with Slides API enabled
- Marp CLI (optional, for Marp format)

## Integration Benefits

### Google Slides vs Other Formats

| Format            | Editability      | Professional      | Sharing       | Collaboration |
| ----------------- | ---------------- | ----------------- | ------------- | ------------- |
| **Google Slides** | ✅ Full          | ✅ Native         | ✅ Link-based | ✅ Real-time  |
| Marp              | ❌ Markdown only | ⚠️ Limited themes | ⚠️ PDF only   | ❌ None       |
| Text              | ❌ Plain text    | ❌ Basic          | ❌ Limited    | ❌ None       |

### Use Cases

- **Team Presentations**: Use `slides` format for collaborative editing
- **Technical Documentation**: Use `marp` format for developer-friendly markdown
- **Quick Prototyping**: Use `txt` format for rapid content development
- **Data Integration**: Use `json` format for custom processing

### Important: API Automation vs Visual Quality

**Key Finding**: Our testing revealed that direct API approaches achieve high technical automation (88-95%) but produce basic presentations requiring extensive manual styling:

- **Generation Time**: 10.2 minutes (very fast)
- **Styling Time**: +15.5 minutes (manual formatting required)
- **Total Time**: 26.2 minutes vs 12 minutes for PDF-carrier workflows
- **Quality Scores**: 63-68% vs 94-96% for PDF workflows

**Recommendation**: Use API workflows for collaborative editing and team sharing, but expect additional styling work for presentation-ready output. For fastest end-to-end automation, consider the [Python-Decktopus workflow](../v1/readme.md).

## Next Steps

For Marp/Decktopus integration, see the [Python-Decktopus workflow](../v1/readme.md).
