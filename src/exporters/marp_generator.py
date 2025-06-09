#!/usr/bin/env python3
"""
Converts Claude-generated slide outlines to Marp-compatible Markdown.
Takes structured text and outputs presentation-ready Markdown.
"""

import re
import sys
import json
from pathlib import Path
from typing import List, Dict, Optional


class MarpGenerator:
    def __init__(self, theme: str = "uncover", background_color: str = "#fff"):
        self.theme = theme
        self.background_color = background_color

    def parse_claude_output(self, text: str) -> List[Dict]:
        """Parse Claude's structured slide output into slide objects."""
        slides = []

        # Split by slide markers
        slide_sections = re.split(r'^SLIDE \d+:', text, flags=re.MULTILINE)

        # Skip first empty split
        for i, section in enumerate(slide_sections[1:], 1):
            slide = self._parse_single_slide(section, i)
            if slide:
                slides.append(slide)

        return slides

    def _parse_single_slide(self, text: str, slide_num: int) -> Optional[Dict]:
        """Parse a single slide section."""
        lines = text.strip().split('\n')
        if not lines:
            return None

        # Extract title (first line)
        title = lines[0].strip()

        # Extract bullet points
        bullets = []
        visual = ""
        speaker_notes = ""

        for line in lines[1:]:
            line = line.strip()
            if line.startswith('•') or line.startswith('-'):
                bullets.append(line.lstrip('•-').strip())
            elif line.startswith('[VISUAL:'):
                visual = re.sub(r'\[VISUAL:\s*(.*?)\]', r'\1', line)
            elif line.startswith('[SPEAKER NOTE:'):
                speaker_notes = re.sub(
                    r'\[SPEAKER NOTE:\s*(.*?)\]', r'\1', line)

        return {
            'number': slide_num,
            'title': title,
            'bullets': bullets,
            'visual': visual,
            'speaker_notes': speaker_notes
        }

    def generate_marp_header(self) -> str:
        """Generate Marp YAML header."""
        return f"""---
marp: true
theme: {self.theme}
paginate: true
backgroundColor: {self.background_color}
class: lead
---

"""

    def slide_to_markdown(self, slide: Dict) -> str:
        """Convert a slide object to Marp markdown."""
        md = f"# {slide['title']}\n\n"

        # Add bullet points
        for bullet in slide['bullets']:
            md += f"- {bullet}\n"

        # Add visual note if present
        if slide['visual']:
            md += f"\n![bg right:40%](https://via.placeholder.com/800x600?text={slide['visual'].replace(' ', '+')})\n"

        # Add speaker notes as HTML comment
        if slide['speaker_notes']:
            md += f"\n<!--\nSpeaker Notes:\n{slide['speaker_notes']}\n-->\n"

        return md

    def generate_marp_presentation(self, slides: List[Dict]) -> str:
        """Generate complete Marp presentation."""
        presentation = self.generate_marp_header()

        for i, slide in enumerate(slides):
            if i > 0:
                presentation += "\n---\n\n"
            presentation += self.slide_to_markdown(slide)

        return presentation


def convert_to_marp(input_file: str, output_file: Optional[str] = None, theme: str = "uncover") -> str:
    """
    Main conversion function.
    """
    # Read input file
    input_path = Path(input_file)
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Generate Marp presentation
    generator = MarpGenerator(theme=theme)
    slides = generator.parse_claude_output(content)

    if not slides:
        raise ValueError(
            "No slides found in input. Make sure input follows 'SLIDE N:' format.")

    marp_content = generator.generate_marp_presentation(slides)

    # Determine output path
    if output_file is None:
        output_path = input_path.parent / f"{input_path.stem}_marp.md"
    else:
        output_path = Path(output_file)

    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(marp_content)

    print(
        f"Generated Marp presentation with {len(slides)} slides -> {output_path}")
    return str(output_path)


def main():
    """Command line interface."""
    if len(sys.argv) < 2:
        print(
            "Usage: python marp_generator.py input_file [output_file] [theme]")
        print("Themes: default, gaia, uncover")
        print("Example: python marp_generator.py claude_output.txt slides.md uncover")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    theme = sys.argv[3] if len(sys.argv) > 3 else "uncover"

    try:
        result = convert_to_marp(input_file, output_file, theme)
        print(f"Marp conversion complete: {result}")
        print("\nTo convert to slides:")
        print(f"marp {Path(result).name} -o {Path(result).stem}.html")
        print(f"marp {Path(result).name} -o {Path(result).stem}.pdf")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
