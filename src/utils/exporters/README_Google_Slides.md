# Google Slides API Integration

This module integrates with **Google Slides API** to convert AI-generated slide content into professional Google Slides presentations with full collaboration features.

## Overview

The Google Slides integration allows you to:

- Convert slide text content to Google Slides presentations
- Create shareable, collaborative presentations
- Leverage Google Workspace ecosystem
- Generate presentations accessible from any device
- Support real-time collaboration

## Setup

### 1. Enable Google Slides API

1. Visit [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the Google Slides API:
   - Go to **APIs & Services** → **Library**
   - Search for "Google Slides API"
   - Click **Enable**

### 2. Create OAuth 2.0 Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **OAuth client ID**
3. Choose **Desktop app** as application type
4. Name your application (e.g., "Intelligence-to-Deck")
5. Download the credentials JSON file
6. Rename it to `credentials.json` and place in your project root

### 3. Install Dependencies

```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

## Usage

### Via Full Workflow

```bash
# Generate Google Slides presentation
python full_workflow.py content.txt --format slides --title "Business Strategy"

# Use with different content types
python full_workflow.py content.txt --type technical --format slides --title "Technical Overview"
```

### Direct Usage

```bash
# Convert slides to Google Slides
python src/exporters/google_slides.py slides.txt "My Presentation Title"

# With custom credentials file
python src/exporters/google_slides.py slides.txt "Presentation" my_credentials.json
```

## Authentication Flow

### First Time Setup

1. Run the script for the first time
2. Browser window will open automatically
3. Sign in to your Google account
4. Grant permissions to the application
5. Authorization complete - `token.json` file created

### Subsequent Runs

- Uses saved `token.json` for authentication
- Automatic token refresh when expired
- No manual intervention required

## Features

### Content Processing

- Automatically parses slide titles and content
- Handles bullet points and structured text
- Preserves hierarchical information
- Supports multiple content formats

### Presentation Creation

- Creates new Google Slides presentations
- Uses professional "Title and Body" layout
- Automatically populates title and content placeholders
- Generates shareable presentation links

### Collaboration Features

- Real-time collaborative editing
- Comment and suggestion system
- Version history and revision tracking
- Sharing controls and permissions

## API Details

### Authentication

- OAuth 2.0 authorization flow
- Secure token-based authentication
- Automatic token refresh
- Local credential storage

### Endpoints

- **Create**: Creates new presentations
- **Update**: Adds slides and content
- **Batch**: Efficient bulk operations

### Permissions Required

- `https://www.googleapis.com/auth/presentations` - Create and edit presentations

## Troubleshooting

### Credentials Issues

```bash
# Check credentials file exists
ls -la credentials.json

# Verify file format (should be valid JSON)
python -c "import json; print(json.load(open('credentials.json'))['type'])"
```

### Authentication Problems

- Delete `token.json` to force re-authentication
- Check Google Account permissions in [Account Settings](https://myaccount.google.com/permissions)
- Verify project OAuth consent screen configuration

### API Errors

- Check Google Cloud Console for API quotas
- Verify Google Slides API is enabled
- Review error messages for specific issues

## Example Workflow

```bash
# 1. Prepare content
echo "Digital Transformation Strategy

Executive Summary:
• Modernize business operations
• Enhance customer experience
• Drive competitive advantage
• Accelerate digital adoption

Key Initiatives:
• Cloud migration strategy
• AI/ML implementation
• Process automation
• Data analytics platform

Expected Outcomes:
• 40% operational efficiency
• 25% cost reduction
• Improved customer satisfaction
• Enhanced market position" > inputs/digital_strategy.txt

# 2. Run workflow
python full_workflow.py digital_strategy.txt --format slides --title "Digital Transformation Strategy"

# 3. Result
# → Google Slides presentation created and shareable link provided
```

## Integration Benefits

### vs. Local File Formats

| Feature                     | Google Slides   | PowerPoint         | PDF          |
| --------------------------- | --------------- | ------------------ | ------------ |
| **Real-time Collaboration** | ✅ Native       | ❌ Limited         | ❌ None      |
| **Version Control**         | ✅ Automatic    | ⚠️ Manual          | ❌ None      |
| **Access Anywhere**         | ✅ Cloud-based  | ⚠️ File-based      | ✅ Universal |
| **Sharing**                 | ✅ Link-based   | ⚠️ File attachment | ✅ Read-only |
| **Comments & Reviews**      | ✅ Integrated   | ⚠️ Limited         | ❌ None      |
| **Mobile Editing**          | ✅ Full support | ⚠️ Limited         | ❌ None      |

### Use Cases

- **Team Presentations**: Real-time collaborative editing
- **Client Proposals**: Easy sharing and commenting
- **Regular Updates**: Version-controlled content
- **Remote Work**: Cloud-based accessibility
- **Mobile Access**: Edit from any device

## Advanced Usage

### Custom Slide Layouts

Modify the `add_slide()` function to use different layouts:

```python
'slideLayoutReference': {
    'predefinedLayout': 'TITLE_ONLY'  # or 'BLANK', 'CAPTION_ONLY', etc.
}
```

### Batch Processing

Process multiple presentations:

```bash
for file in inputs/*.txt; do
    title=$(basename "$file" .txt | tr '_' ' ' | sed 's/\b\w/\U&/g')
    python full_workflow.py $(basename "$file") --format slides --title "$title"
done
```

### Theme and Styling

Apply custom themes programmatically:

```python
# Add after presentation creation
requests = [{
    'updatePresentationProperties': {
        'presentationProperties': {
            'title': title
        },
        'fields': 'title'
    }
}]
```

## Security and Privacy

### Data Handling

- Content processed through Google Slides API
- Data stored in your Google Drive
- Subject to Google Workspace security policies
- No third-party data storage

### Access Control

- OAuth 2.0 secure authentication
- Granular sharing permissions
- Link-based or user-specific access
- Integration with Google Workspace admin controls

## Error Handling

### Common Issues

1. **Quota Exceeded**: Check API limits in Google Cloud Console
2. **Invalid Credentials**: Re-download credentials.json
3. **Permission Denied**: Verify OAuth scopes
4. **Network Issues**: Check internet connectivity

### Debug Mode

Enable verbose logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Limitations

- Requires internet connection
- Google account required
- Subject to Google API quotas
- Text-based content only (no advanced formatting)

## Support Resources

- **Google Slides API Documentation**: https://developers.google.com/slides/api
- **Python Client Library**: https://github.com/googleapis/google-api-python-client
- **Samples and Examples**: https://developers.google.com/slides/api/samples
- **Stack Overflow**: Tag with `google-slides-api`

## License

This integration module follows the same license as the main project. Google Slides API usage is subject to Google's Terms of Service.
