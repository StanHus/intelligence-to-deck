# Workflow Documentation Hub

This directory contains validated workflows for AI-powered presentation automation, tested across 17 tools with 200+ production presentations.

## Quick Links

### 🚀 Primary Workflows

- **[Claude → Decktopus](./claude-decktopus/)** - Manual workflow (15 min → 12 min)
- **[Python → Decktopus](./python-decktopus/)** - Automated workflow (12±2 min)

### 🔍 Alternative Workflows

- **[Claude → Canva](./claude-canva/)** - Design-focused (5 min design + 30 min content)
- **[Notion → Google Slides](./notion-google_slides/)** - Privacy-compliant (25-30 min)

## Performance Summary

| Workflow           | Time   | Accuracy | Content Population | Use Case          |
| ------------------ | ------ | -------- | ------------------ | ----------------- |
| Claude → Decktopus | 15 min | 94-96%   | 94%                | Manual production |
| Python → Decktopus | 12 min | 94-96%   | 94%                | Automated/scale   |
| Claude → Canva     | 35 min | 88%      | <30%               | Design-heavy      |
| Notion → Slides    | 27 min | 94%      | 85%                | Privacy-first     |

## Key Findings

### ✅ Success Factors

- **PDF-carrier pattern**: Preserves 85% better semantic structure vs. direct text
- **Content-first approach**: 94% automation vs. <30% for design-first tools
- **Python preprocessing**: 40% time reduction on documents >10K words

### 🎯 Quality Thresholds

- **Minimum viable accuracy**: 94% (client satisfaction jumps to 9.2/10)
- **Automation completeness**: >90% (tools below this are template engines)
- **Time target**: <20 minutes end-to-end

## Repository Structure

```
workflows/
├── claude-decktopus/          # Manual workflow
│   ├── prompt.txt             # Claude prompts
│   ├── decktopus-output.pdf   # Sample output
│   └── *.png                  # Process screenshots
├── python-decktopus/          # Automated workflow
│   ├── python-workflow.png    # Process diagram
│   └── decktopus-output.pdf   # Sample output
├── claude-canva/              # Design-focused alternative
└── notion-google_slides/      # Privacy-compliant alternative
```

## Implementation Guides

### Quick Start (30 minutes)

1. **Clone repository**: `git clone https://github.com/StanHus/intelligence-to-deck`
2. **Choose workflow**: Start with [claude-decktopus](./claude-decktopus/) for manual testing
3. **Scale up**: Move to [python-decktopus](./python-decktopus/) for automation
4. **Review methodology**: See [../methodology.md](../methodology.md) for validation details

### ROI Calculator

- **Time savings**: 156 hours/analyst/year (4+ decks/week)
- **Cost impact**: $31,200 additional annual capacity per analyst
- **Quality maintained**: 94-96% across 200 production decks

## External Validation

| Source            | Finding                                   | Link                                                                        |
| ----------------- | ----------------------------------------- | --------------------------------------------------------------------------- |
| Indico Labs       | 60-80% time reduction with PDF automation | [Blog Post](https://www.indicolabs.io/blog/powerpoint-automation-use-cases) |
| Forrester TEI     | 248% ROI on workflow automation           | Industry Research                                                           |
| Independent Teams | 92% efficiency replication in <30 min     | Repository artifacts                                                        |

---

**Last Updated**: January 2025  
**Owner**: AI Center of Excellence  
**Questions?** See [../methodology.md](../methodology.md) or open an issue
