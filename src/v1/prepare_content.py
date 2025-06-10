#!/usr/bin/env python3
"""
Text preprocessing utility for the Intelligence-to-Deck pipeline.
Handles cleaning and intelligent chunking of large documents.
"""

import re
import sys
from pathlib import Path
from typing import List, Optional


class TextPreprocessor:
    def __init__(self, max_chunk_size: int = 45000):
        self.max_chunk_size = max_chunk_size

    def clean_text(self, text: str) -> str:
        """Clean and normalize text content."""
        # Remove excessive whitespace
        text = ' '.join(text.split())

        # Remove special characters that might break formatting
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', '', text)

        # Normalize line endings
        text = text.replace('\r\n', '\n').replace('\r', '\n')

        # Fix common transcript artifacts
        text = re.sub(r'\[inaudible\]', '[UNCLEAR]', text, flags=re.IGNORECASE)
        text = re.sub(r'\[crosstalk\]', '[OVERLAP]', text, flags=re.IGNORECASE)

        return text.strip()

    def find_natural_breaks(self, text: str) -> List[int]:
        """Find natural break points in text (headers, paragraphs, etc.)."""
        break_points = []

        # Look for markdown headers
        for match in re.finditer(r'^#{1,6}\s.*$', text, re.MULTILINE):
            break_points.append(match.start())

        # Look for section breaks
        for match in re.finditer(r'\n\s*---+\s*\n', text):
            break_points.append(match.start())

        # Look for paragraph breaks (double newlines)
        for match in re.finditer(r'\n\s*\n', text):
            break_points.append(match.start())

        return sorted(set(break_points))

    def smart_chunk_document(self, text: str) -> List[str]:
        """
        Intelligently chunk document while preserving context.
        Returns list of text chunks suitable for Claude processing.
        """
        if len(text) <= self.max_chunk_size:
            return [text]

        chunks = []
        current_chunk = ""
        break_points = self.find_natural_breaks(text)
        last_break = 0

        for break_point in break_points:
            # Get text from last break to current break
            section = text[last_break:break_point]

            # If adding this section would exceed chunk size, finalize current chunk
            if len(current_chunk) + len(section) > self.max_chunk_size and current_chunk:
                current_chunk += "\n\n[CONTINUED IN NEXT SECTION]"
                chunks.append(current_chunk.strip())
                current_chunk = "[CONTINUING FROM PREVIOUS SECTION]\n\n"

            current_chunk += section
            last_break = break_point

        # Add remaining text
        remaining = text[last_break:]
        if remaining:
            current_chunk += remaining

        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        return chunks


def prepare_content(input_file: str, output_file: Optional[str] = None) -> str:
    """
    Main function to prepare content for Claude processing.
    Returns the output file path.
    """
    # Read input file
    input_path = Path(input_file)
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Initialize preprocessor
    preprocessor = TextPreprocessor()

    # Clean and chunk the content
    cleaned_text = preprocessor.clean_text(content)
    chunks = preprocessor.smart_chunk_document(cleaned_text)

    # Determine output path
    if output_file is None:
        output_path = input_path.parent / \
            f"{input_path.stem}_prepared{input_path.suffix}"
    else:
        output_path = Path(output_file)

    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        if len(chunks) == 1:
            # Single chunk
            f.write(chunks[0])
        else:
            # Multiple chunks with separators
            for i, chunk in enumerate(chunks, 1):
                f.write(f"=== CHUNK {i} OF {len(chunks)} ===\n\n")
                f.write(chunk)
                f.write("\n\n")

    print(f"Processed {len(chunks)} chunk(s) -> {output_path}")
    return str(output_path)


def main():
    """Command line interface."""
    if len(sys.argv) < 2:
        print("Usage: python prepare_content.py input_file [output_file]")
        print("Example: python prepare_content.py transcript.txt prepared.txt")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        result = prepare_content(input_file, output_file)
        print(f"Content preparation complete: {result}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
