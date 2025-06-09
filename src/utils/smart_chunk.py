#!/usr/bin/env python3
"""
Advanced document chunking utility with token counting and semantic awareness.
Handles various input formats and provides multiple chunking strategies.
"""

import re
import sys
import json
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass


@dataclass
class ChunkMetadata:
    """Metadata for each chunk."""
    chunk_id: int
    start_pos: int
    end_pos: int
    token_count: int
    content_type: str
    has_headers: bool
    has_data: bool


class SmartChunker:
    def __init__(self,
                 max_tokens: int = 15000,
                 overlap_tokens: int = 200,
                 min_chunk_size: int = 1000):
        self.max_tokens = max_tokens
        self.overlap_tokens = overlap_tokens
        self.min_chunk_size = min_chunk_size

    def estimate_tokens(self, text: str) -> int:
        """Rough token estimation (1 token ≈ 4 characters for English)."""
        return len(text) // 4

    def detect_content_type(self, text: str) -> str:
        """Detect the type of content for better chunking strategy."""
        # Check for various content patterns
        if re.search(r'```|```python|```javascript', text):
            return "technical"
        elif re.search(r'Q:|A:|Speaker \d+:|INTERVIEWER:', text):
            return "interview"
        elif re.search(r'#{1,6}\s', text):
            return "markdown"
        elif re.search(r'\d+\.\s|\*\s|-\s', text):
            return "structured"
        else:
            return "prose"

    def find_semantic_breaks(self, text: str, content_type: str) -> List[int]:
        """Find semantic break points based on content type."""
        breaks = []

        if content_type == "interview":
            # Break on speaker changes
            for match in re.finditer(r'^(Q:|A:|Speaker \d+:|INTERVIEWER:|RESPONDENT:)', text, re.MULTILINE):
                breaks.append(match.start())

        elif content_type == "markdown":
            # Break on headers
            for match in re.finditer(r'^#{1,6}\s.*$', text, re.MULTILINE):
                breaks.append(match.start())

        elif content_type == "technical":
            # Break on code blocks and sections
            for match in re.finditer(r'^```|^##\s|^###\s', text, re.MULTILINE):
                breaks.append(match.start())

        # Always include paragraph breaks
        for match in re.finditer(r'\n\s*\n', text):
            breaks.append(match.start())

        return sorted(set(breaks))

    def chunk_with_overlap(self, text: str) -> List[Tuple[str, ChunkMetadata]]:
        """Create overlapping chunks for better context preservation."""
        content_type = self.detect_content_type(text)
        break_points = self.find_semantic_breaks(text, content_type)

        chunks = []
        start_idx = 0
        chunk_id = 1

        while start_idx < len(text):
            # Find the end point for this chunk
            # Convert tokens to chars
            end_idx = start_idx + (self.max_tokens * 4)

            # Adjust end to nearest semantic break
            if end_idx < len(text):
                suitable_breaks = [
                    bp for bp in break_points if start_idx < bp <= end_idx]
                if suitable_breaks:
                    end_idx = suitable_breaks[-1]
            else:
                end_idx = len(text)

            # Extract chunk text
            chunk_text = text[start_idx:end_idx].strip()

            # Skip tiny chunks
            if len(chunk_text) < self.min_chunk_size and chunk_id > 1:
                break

            # Create metadata
            metadata = ChunkMetadata(
                chunk_id=chunk_id,
                start_pos=start_idx,
                end_pos=end_idx,
                token_count=self.estimate_tokens(chunk_text),
                content_type=content_type,
                has_headers=bool(
                    re.search(r'^#{1,6}\s', chunk_text, re.MULTILINE)),
                has_data=bool(re.search(r'\d+%|\$\d+|\d+,\d+', chunk_text))
            )

            # Add context bridges
            if chunk_id > 1:
                chunk_text = f"[CONTEXT: This continues from previous section]\n\n{chunk_text}"

            if end_idx < len(text):
                chunk_text = f"{chunk_text}\n\n[CONTINUES: This section continues in next chunk]"

            chunks.append((chunk_text, metadata))

            # Calculate next start position with overlap
            next_start = end_idx - (self.overlap_tokens * 4)
            start_idx = max(next_start, start_idx + self.min_chunk_size)
            chunk_id += 1

        return chunks

    def chunk_by_sections(self, text: str) -> List[Tuple[str, ChunkMetadata]]:
        """Chunk by logical sections (headers, speakers, etc.)."""
        content_type = self.detect_content_type(text)
        break_points = self.find_semantic_breaks(text, content_type)

        if not break_points:
            return self.chunk_with_overlap(text)

        chunks = []
        chunk_id = 1

        # Add start of document
        break_points = [0] + break_points + [len(text)]

        for i in range(len(break_points) - 1):
            start_idx = break_points[i]
            end_idx = break_points[i + 1]

            section_text = text[start_idx:end_idx].strip()

            # If section is too large, sub-chunk it
            if self.estimate_tokens(section_text) > self.max_tokens:
                sub_chunks = self.chunk_with_overlap(section_text)
                for sub_text, sub_meta in sub_chunks:
                    sub_meta.chunk_id = chunk_id
                    chunks.append((sub_text, sub_meta))
                    chunk_id += 1
            else:
                metadata = ChunkMetadata(
                    chunk_id=chunk_id,
                    start_pos=start_idx,
                    end_pos=end_idx,
                    token_count=self.estimate_tokens(section_text),
                    content_type=content_type,
                    has_headers=bool(
                        re.search(r'^#{1,6}\s', section_text, re.MULTILINE)),
                    has_data=bool(
                        re.search(r'\d+%|\$\d+|\d+,\d+', section_text))
                )
                chunks.append((section_text, metadata))
                chunk_id += 1

        return chunks


def smart_chunk_file(input_file: str,
                     output_file: Optional[str] = None,
                     strategy: str = "overlap",
                     max_tokens: int = 15000,
                     format_output: str = "text") -> str:
    """
    Main chunking function with multiple strategies.

    Args:
        input_file: Path to input file
        output_file: Path to output file (optional)
        strategy: "overlap" or "sections"
        max_tokens: Maximum tokens per chunk
        format_output: "text", "json", or "markdown"
    """
    # Read input
    input_path = Path(input_file)
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Initialize chunker
    chunker = SmartChunker(max_tokens=max_tokens)

    # Choose chunking strategy
    if strategy == "sections":
        chunks = chunker.chunk_by_sections(content)
    else:
        chunks = chunker.chunk_with_overlap(content)

    # Determine output path
    if output_file is None:
        suffix = f"_{format_output}" if format_output != "text" else ""
        ext = ".json" if format_output == "json" else ".md" if format_output == "markdown" else ".txt"
        output_path = input_path.parent / \
            f"{input_path.stem}_chunked{suffix}{ext}"
    else:
        output_path = Path(output_file)

    # Format and write output
    if format_output == "json":
        output_data = {
            "metadata": {
                "total_chunks": len(chunks),
                "strategy": strategy,
                "max_tokens": max_tokens,
                "source_file": str(input_path)
            },
            "chunks": [
                {
                    "text": text,
                    "metadata": {
                        "chunk_id": meta.chunk_id,
                        "token_count": meta.token_count,
                        "content_type": meta.content_type,
                        "has_headers": meta.has_headers,
                        "has_data": meta.has_data
                    }
                }
                for text, meta in chunks
            ]
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)

    elif format_output == "markdown":
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"# Chunked Document: {input_path.name}\n\n")
            f.write(
                f"**Strategy:** {strategy} | **Max Tokens:** {max_tokens} | **Total Chunks:** {len(chunks)}\n\n")

            for text, meta in chunks:
                f.write(f"## Chunk {meta.chunk_id}\n\n")
                f.write(
                    f"**Tokens:** {meta.token_count} | **Type:** {meta.content_type}\n\n")
                f.write(f"{text}\n\n")
                f.write("---\n\n")

    else:  # text format
        with open(output_path, 'w', encoding='utf-8') as f:
            for i, (text, meta) in enumerate(chunks):
                if i > 0:
                    f.write(f"\n{'='*50}\n")
                f.write(
                    f"CHUNK {meta.chunk_id} | {meta.token_count} tokens | {meta.content_type}\n")
                f.write(f"{'='*50}\n\n")
                f.write(text)
                f.write("\n\n")

    print(f"Created {len(chunks)} chunks -> {output_path}")
    return str(output_path)


def main():
    """Command line interface."""
    if len(sys.argv) < 2:
        print("Usage: python smart_chunk.py input_file [options]")
        print("Options:")
        print("  --output FILE       Output file path")
        print("  --strategy STRAT    'overlap' or 'sections' (default: overlap)")
        print("  --max-tokens N      Maximum tokens per chunk (default: 15000)")
        print("  --format FORMAT     'text', 'json', or 'markdown' (default: text)")
        print("\nExample:")
        print("  python smart_chunk.py document.txt --strategy sections --format json")
        sys.exit(1)

    # Parse arguments
    input_file = sys.argv[1]
    output_file = None
    strategy = "overlap"
    max_tokens = 15000
    format_output = "text"

    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "--output" and i + 1 < len(sys.argv):
            output_file = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--strategy" and i + 1 < len(sys.argv):
            strategy = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--max-tokens" and i + 1 < len(sys.argv):
            max_tokens = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == "--format" and i + 1 < len(sys.argv):
            format_output = sys.argv[i + 1]
            i += 2
        else:
            print(f"Unknown argument: {sys.argv[i]}")
            sys.exit(1)

    try:
        result = smart_chunk_file(
            input_file, output_file, strategy, max_tokens, format_output)
        print(f"Smart chunking complete: {result}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
