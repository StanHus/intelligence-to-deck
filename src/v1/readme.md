# Intelligence-to-Deck Python Scripts (v1)

## Python-Decktopus Workflow

**This is the original workflow optimized for Marp/Decktopus integration.**

Python utilities for converting documents to presentation slides via AI workflows with Marp output for Decktopus PDF import.

## Setup

```bash
# Install OpenAI package
pip install openai

# Install Marp CLI
npm install -g @marp-team/marp-cli

# Set API key
export OPENAI_API_KEY="your-api-key-here"
```

## Usage

### Complete Workflow (Python-Decktopus)

```bash
# Basic usage
python src/v1/full_workflow.py input.txt --type business --format marp

# With theme selection
python src/v1/full_workflow.py input.txt --type business --format marp --theme uncover
```

### Individual Components

```bash
# Text preprocessing
python src/v1/prepare_content.py input.txt clean.txt

# Slide generation (15-20 slides)
python src/v1/generate_slides.py clean.txt --type business

# Marp conversion
python src/utils/exporters/marp_generator.py slides.txt presentation.md
```

## Options

**Content Types**: `business`, `technical`, `general`  
**Output Formats**: `txt`, `marp`, `json`  
**Models**: `gpt-4-turbo` (default), `gpt-4`

## File Structure

```
├── inputs/                     # Source documents
├── outputs/                    # Generated presentations
├── src/
│   └── v1/                    # Python-Decktopus workflow
│       ├── full_workflow.py   # Complete automation
│       ├── prepare_content.py # Text preprocessing
│       ├── generate_slides.py # AI slide generation
│       └── readme.md          # This file
│   └── utils/
│       └── exporters/
│           └── marp_generator.py # Marp markdown export
```

## Complete Automated Workflow

```bash
# One command to rule them all - Python-Decktopus
python src/v1/full_workflow.py script_1.txt

# Or with options
python src/v1/full_workflow.py script_1.txt --type business --format marp --theme uncover
```

This runs the entire pipeline:

1. **Prepare**: Clean and chunk content
2. **Generate**: Create slides with OpenAI
3. **Convert**: Transform to Marp markdown
4. **Export**: Generate final PDF

## Individual Scripts

### Text Preprocessing

```bash
python src/v1/prepare_content.py input.txt [output.txt]
```

### AI Slide Generation

```bash
python src/v1/generate_slides.py prepared.txt --type business --model gpt-4-turbo
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

- `marp`: Automated markdown → PDF generation (recommended for Decktopus)
- `txt`: Plain text slides
- `json`: Structured slide data

**Models**:

- `gpt-4-turbo`: Best quality, moderate cost
- `gpt-4`: Highest quality, higher cost
- `gpt-3.5-turbo`: Fast and cheap

## Cost Estimation

```bash
# See cost before running
python src/v1/generate_slides.py input.txt --dry-run
```

Typical costs:

- Short transcript (2K words): ~$0.15
- Long document (10K words): ~$0.75
- Research report (20K words): ~$1.50

## Example with script_1.txt

```bash
# Complete automation - Python-Decktopus workflow
python src/v1/full_workflow.py script_1.txt --type business --format marp

# Manual steps
python src/v1/prepare_content.py script_1.txt clean.txt
python src/v1/generate_slides.py clean.txt --type business
python src/utils/exporters/marp_generator.py clean_slides.txt slides.md
marp slides.md -o presentation.pdf
```

## Requirements

- Python 3.7+
- OpenAI API key
- Marp CLI for final conversion

## Decktopus Integration

This workflow is optimized for importing generated PDFs into Decktopus:

1. Generate Marp slides: `python src/v1/full_workflow.py input.txt --format marp`
2. Convert to PDF: `marp outputs/input_presentation.md -o outputs/input.pdf`
3. Import PDF into Decktopus for final styling and edits

## Next Steps

For Google Slides integration, see the [Python-Slides workflow](../v2/readme.md).
