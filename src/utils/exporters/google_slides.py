#!/usr/bin/env python3
"""
Google Slides API Integration Module
Integrates with Google Slides API to convert slide content into 
professional Google Slides presentations.

Features:
- Smaller, more compact fonts (12pt body, 24pt titles)
- Clean Arial font family
- Optimized line spacing for better content density
- Professional formatting
"""

import os
import json
import re
import pickle
from pathlib import Path
from typing import Dict, List, Optional, Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GoogleSlidesClient:
    """Client for Google Slides API integration."""

    # Scopes required for creating and editing presentations
    SCOPES = ['https://www.googleapis.com/auth/presentations']

    def __init__(self, credentials_file: str = "credentials.json"):
        self.credentials_file = credentials_file
        self.token_file = "token.json"
        self.service = None
        self.creds = None

    def authenticate(self) -> bool:
        """Authenticate with Google Slides API."""
        print("🔐 Authenticating with Google Slides API...")

        # Check if credentials file exists
        if not os.path.exists(self.credentials_file):
            print(f"❌ Credentials file not found: {self.credentials_file}")
            print("💡 Download credentials.json from Google Cloud Console:")
            print("   1. Go to https://console.cloud.google.com/")
            print("   2. Enable Google Slides API")
            print("   3. Create OAuth 2.0 credentials")
            print("   4. Download as credentials.json")
            return False

        # Load existing token if available
        if os.path.exists(self.token_file):
            self.creds = Credentials.from_authorized_user_file(
                self.token_file, self.SCOPES)

        # If there are no (valid) credentials available, let the user log in
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, self.SCOPES)
                self.creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open(self.token_file, 'w') as token:
                token.write(self.creds.to_json())

        try:
            self.service = build('slides', 'v1', credentials=self.creds)
            print("✅ Authentication successful")
            return True
        except Exception as e:
            print(f"❌ Authentication failed: {e}")
            return False

    def parse_slides_content(self, slides_file: Path) -> List[Dict[str, Any]]:
        """Parse slides content from text file into structured data."""
        print(f"📖 Parsing slides content from {slides_file}...")

        try:
            with open(slides_file, 'r', encoding='utf-8') as f:
                content = f.read()

            slides = []
            # Split content by slide markers
            slide_blocks = re.split(r'SLIDE \d+:', content)[1:]

            for i, block in enumerate(slide_blocks, 1):
                lines = [line.strip()
                         for line in block.strip().split('\n') if line.strip()]

                if not lines:
                    continue

                # First line is usually the title
                title = lines[0] if lines else f"Slide {i}"

                # Rest is content, join with newlines for bullet points
                content_lines = lines[1:] if len(lines) > 1 else []

                # Process bullet points
                bullet_points = []
                current_content = []

                for line in content_lines:
                    if line.startswith(('•', '-', '*')) or re.match(r'^\d+\.', line):
                        if current_content:
                            bullet_points.append(' '.join(current_content))
                            current_content = []
                        # Clean bullet point markers
                        clean_line = re.sub(r'^[•\-\*]\s*', '', line)
                        clean_line = re.sub(r'^\d+\.\s*', '', clean_line)
                        bullet_points.append(clean_line)
                    else:
                        current_content.append(line)

                # Add remaining content
                if current_content:
                    bullet_points.append(' '.join(current_content))

                slide_data = {
                    "slide_number": i,
                    "title": title,
                    "content": bullet_points,
                    "full_content": '\n'.join(lines)
                }
                slides.append(slide_data)

            print(f"✅ Parsed {len(slides)} slides")
            return slides

        except Exception as e:
            print(f"❌ Error parsing slides: {e}")
            return []

    def create_presentation(self, title: str) -> Optional[str]:
        """Create a new Google Slides presentation."""
        try:
            presentation = {
                'title': title
            }

            presentation = self.service.presentations().create(body=presentation).execute()
            presentation_id = presentation.get('presentationId')

            print(f"✅ Created presentation: {title}")
            print(f"📄 Presentation ID: {presentation_id}")

            return presentation_id

        except HttpError as e:
            print(f"❌ Error creating presentation: {e}")
            return None

    def add_slide(self, presentation_id: str, slide_data: Dict[str, Any]) -> bool:
        """Add a slide with title and content to the presentation."""
        try:
            # Create slide
            slide_id = f"slide_{slide_data['slide_number']}"

            requests = [
                {
                    'createSlide': {
                        'objectId': slide_id,
                        'slideLayoutReference': {
                            'predefinedLayout': 'TITLE_AND_BODY'
                        }
                    }
                }
            ]

            # Execute slide creation
            self.service.presentations().batchUpdate(
                presentationId=presentation_id,
                body={'requests': requests}
            ).execute()

            # Add content to the slide
            content_requests = []
            formatting_requests = []

            # Add title
            title_placeholder_id = None
            body_placeholder_id = None

            # Get slide to find placeholder IDs
            presentation = self.service.presentations().get(
                presentationId=presentation_id
            ).execute()

            slides = presentation.get('slides', [])
            current_slide = None

            for slide in slides:
                if slide.get('objectId') == slide_id:
                    current_slide = slide
                    break

            if current_slide:
                page_elements = current_slide.get('pageElements', [])
                for element in page_elements:
                    if 'shape' in element:
                        shape = element['shape']
                        if 'placeholder' in shape:
                            placeholder_type = shape['placeholder'].get('type')
                            if placeholder_type == 'TITLE':
                                title_placeholder_id = element['objectId']
                            elif placeholder_type == 'BODY':
                                body_placeholder_id = element['objectId']

            # Insert title
            if title_placeholder_id:
                content_requests.append({
                    'insertText': {
                        'objectId': title_placeholder_id,
                        'text': slide_data['title']
                    }
                })
                # Format title with smaller font
                formatting_requests.append({
                    'updateTextStyle': {
                        'objectId': title_placeholder_id,
                        'style': {
                            'fontSize': {
                                'magnitude': 24,  # Smaller title font
                                'unit': 'PT'
                            },
                            'fontFamily': 'Arial',
                            'bold': True
                        },
                        'fields': 'fontSize,fontFamily,bold'
                    }
                })

            # Insert content
            if body_placeholder_id and slide_data['content']:
                content_text = '\n'.join(
                    [f"• {item}" for item in slide_data['content']])
                content_requests.append({
                    'insertText': {
                        'objectId': body_placeholder_id,
                        'text': content_text
                    }
                })
                # Format body text with smaller font
                formatting_requests.append({
                    'updateTextStyle': {
                        'objectId': body_placeholder_id,
                        'style': {
                            'fontSize': {
                                'magnitude': 12,  # Much smaller body font
                                'unit': 'PT'
                            },
                            'fontFamily': 'Arial'
                        },
                        'fields': 'fontSize,fontFamily'
                    }
                })

            # Execute content insertion first
            if content_requests:
                self.service.presentations().batchUpdate(
                    presentationId=presentation_id,
                    body={'requests': content_requests}
                ).execute()

            # Then apply formatting
            if formatting_requests:
                self.service.presentations().batchUpdate(
                    presentationId=presentation_id,
                    body={'requests': formatting_requests}
                ).execute()

            return True

        except HttpError as e:
            print(f"❌ Error adding slide {slide_data['slide_number']}: {e}")
            return False

    def generate_presentation(self, slides_file: Path, presentation_title: str) -> Optional[str]:
        """Generate Google Slides presentation from slides content."""

        if not self.service:
            if not self.authenticate():
                return None

        # Parse slides content
        slides = self.parse_slides_content(slides_file)
        if not slides:
            print("❌ No slides to process")
            return None

        print(
            f"🚀 Generating Google Slides presentation with {len(slides)} slides...")

        # Create presentation
        presentation_id = self.create_presentation(presentation_title)
        if not presentation_id:
            return None

        # Add slides (skip first slide as it's created by default)
        success_count = 0

        # Update the first slide (already exists)
        if slides:
            first_slide = slides[0]
            try:
                # Get the default slide
                presentation = self.service.presentations().get(
                    presentationId=presentation_id
                ).execute()

                default_slide = presentation.get('slides', [{}])[0]
                slide_id = default_slide.get('objectId')

                if slide_id:
                    # Find placeholders and update content
                    content_requests = []
                    formatting_requests = []
                    page_elements = default_slide.get('pageElements', [])

                    title_placeholder_id = None
                    body_placeholder_id = None

                    for element in page_elements:
                        if 'shape' in element:
                            shape = element['shape']
                            if 'placeholder' in shape:
                                placeholder_type = shape['placeholder'].get(
                                    'type')
                                if placeholder_type == 'TITLE':
                                    title_placeholder_id = element['objectId']
                                    content_requests.append({
                                        'insertText': {
                                            'objectId': element['objectId'],
                                            'text': first_slide['title']
                                        }
                                    })
                                    # Format title
                                    formatting_requests.append({
                                        'updateTextStyle': {
                                            'objectId': element['objectId'],
                                            'style': {
                                                'fontSize': {
                                                    'magnitude': 24,  # Smaller title font
                                                    'unit': 'PT'
                                                },
                                                'fontFamily': 'Arial',
                                                'bold': True
                                            },
                                            'fields': 'fontSize,fontFamily,bold'
                                        }
                                    })
                                elif placeholder_type == 'BODY':
                                    body_placeholder_id = element['objectId']
                                    if first_slide['content']:
                                        content_text = '\n'.join(
                                            [f"• {item}" for item in first_slide['content']])
                                        content_requests.append({
                                            'insertText': {
                                                'objectId': element['objectId'],
                                                'text': content_text
                                            }
                                        })
                                        # Format body text
                                        formatting_requests.append({
                                            'updateTextStyle': {
                                                'objectId': element['objectId'],
                                                'style': {
                                                    'fontSize': {
                                                        'magnitude': 12,  # Much smaller body font
                                                        'unit': 'PT'
                                                    },
                                                    'fontFamily': 'Arial'
                                                },
                                                'fields': 'fontSize,fontFamily'
                                            }
                                        })

                    # Execute content insertion first
                    if content_requests:
                        self.service.presentations().batchUpdate(
                            presentationId=presentation_id,
                            body={'requests': content_requests}
                        ).execute()

                    # Then apply formatting
                    if formatting_requests:
                        self.service.presentations().batchUpdate(
                            presentationId=presentation_id,
                            body={'requests': formatting_requests}
                        ).execute()

                        success_count += 1

            except Exception as e:
                print(f"❌ Error updating first slide: {e}")

        # Add remaining slides
        for slide in slides[1:]:
            if self.add_slide(presentation_id, slide):
                success_count += 1
            else:
                print(f"⚠️  Failed to add slide {slide['slide_number']}")

        print(f"✅ Successfully created {success_count}/{len(slides)} slides")

        # Generate shareable link
        presentation_url = f"https://docs.google.com/presentation/d/{presentation_id}/edit"
        print(f"🔗 Presentation URL: {presentation_url}")

        return presentation_id


def main():
    """CLI interface for Google Slides integration."""
    import sys

    if len(sys.argv) < 3:
        print(
            "Usage: python google_slides.py <slides_file> <presentation_title> [credentials_file]")
        print("\nSetup required:")
        print("1. Enable Google Slides API in Google Cloud Console")
        print("2. Create OAuth 2.0 credentials")
        print("3. Download credentials.json file")
        print("\nExample:")
        print("  python google_slides.py slides.txt 'My Presentation'")
        print("  python google_slides.py slides.txt 'Business Plan' my_credentials.json")
        sys.exit(1)

    slides_file = Path(sys.argv[1])
    presentation_title = sys.argv[2]
    credentials_file = sys.argv[3] if len(sys.argv) > 3 else "credentials.json"

    if not slides_file.exists():
        print(f"❌ Error: Slides file not found: {slides_file}")
        sys.exit(1)

    client = GoogleSlidesClient(credentials_file)
    presentation_id = client.generate_presentation(
        slides_file, presentation_title)

    if presentation_id:
        print(f"\n✅ Success! Presentation created with ID: {presentation_id}")
        print(
            f"🔗 View at: https://docs.google.com/presentation/d/{presentation_id}/edit")
        sys.exit(0)
    else:
        print("❌ Failed to create presentation")
        sys.exit(1)


if __name__ == "__main__":
    main()
