# Intelligence-to-Deck Python Scripts

Python utilities for converting documents to presentation slides via AI workflows.

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

### Complete Workflow

```bash
python src/full_workflow.py input.txt --type business --format txt
```

### Individual Components

```bash
# Text preprocessing
python src/prepare_content.py input.txt clean.txt

# Slide generation (15-20 slides)
python src/generate_slides.py clean.txt --type business

# Marp conversion
python src/exporters/marp_generator.py slides.txt presentation.md
```

## Options

**Content Types**: `business`, `technical`, `general`  
**Output Formats**: `txt`, `marp`, `json`  
**Models**: `gpt-4-turbo` (default), `gpt-4`

## File Structure

## Complete Automated Workflow

```bash
# One command to rule them all
python src/full_workflow.py script_1.txt

# Or with options
python src/full_workflow.py script_1.txt --type business --format marp --theme uncover
```

This runs the entire pipeline:

1. **Prepare**: Clean and chunk content
2. **Generate**: Create slides with OpenAI
3. **Convert**: Transform to Marp markdown
4. **Export**: Generate final PDF

## Individual Scripts

### Text Preprocessing

```bash
python src/prepare_content.py input.txt [output.txt]
```

### AI Slide Generation

```bash
python src/generate_slides.py prepared.txt --type business --model gpt-4-turbo
```

### Marp Conversion

```bash
python src/exporters/marp_generator.py slides.txt presentation.md uncover
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

- `marp`: Automated markdown → PDF generation
- `decktopus`: Formatted for PDF import

**Models**:

- `gpt-4-turbo`: Best quality, moderate cost
- `gpt-4`: Highest quality, higher cost
- `gpt-3.5-turbo`: Fast and cheap

## Cost Estimation

```bash
# See cost before running
python src/generate_slides.py input.txt --dry-run
```

Typical costs:

- Short transcript (2K words): ~$0.15
- Long document (10K words): ~$0.75
- Research report (20K words): ~$1.50

## Example with script_1.txt

```bash
# Complete automation
python src/full_workflow.py script_1.txt --type business

# Manual steps
python src/prepare_content.py script_1.txt clean.txt
python src/generate_slides.py clean.txt --type business
python src/exporters/marp_generator.py clean_slides.txt slides.md
marp slides.md -o presentation.pdf
```

## Requirements

- Python 3.7+
- OpenAI API key
- Marp CLI for final conversion
