#!/usr/bin/env python3
"""
Complete Intelligence-to-Deck workflow automation.
Processes raw content → cleaned content → AI slides → formatted output.
Uses inputs/ and outputs/ directory structure.
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import Optional


def setup_directories():
    """Create inputs and outputs directories if they don't exist."""
    inputs_dir = Path("inputs")
    outputs_dir = Path("outputs")

    inputs_dir.mkdir(exist_ok=True)
    outputs_dir.mkdir(exist_ok=True)

    print("📁 Directory structure ready:")
    print(f"   • inputs/ - Place your source files here")
    print(f"   • outputs/ - Generated presentations will be saved here")


def run_command(cmd: list, description: str) -> bool:
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    print(f"🐛 DEBUG: Running command: {' '.join(cmd)}")
    try:
        # Remove capture_output to see real-time progress
        result = subprocess.run(cmd, check=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in {description}: {e}")
        print(f"🐛 DEBUG: Return code: {e.returncode}")
        if hasattr(e, 'stdout') and e.stdout:
            print(f"stdout: {e.stdout}")
        if hasattr(e, 'stderr') and e.stderr:
            print(f"stderr: {e.stderr}")
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python full_workflow.py <input_filename> [options]")
        print("\nDirectory Structure:")
        print("  • Place input files in: inputs/")
        print("  • All outputs saved to: outputs/")
        print("\nOptions:")
        print("  --type business|technical    Content type (default: business)")
        print("  --format marp|txt|json      Output format (default: txt)")
        print("  --theme default|gaia        Marp theme (default: default)")
        print("\nExamples:")
        print("  python full_workflow.py script_1.txt")
        print("  python full_workflow.py transcript.txt --type technical --format marp")
        print("\nFile locations:")
        print("  Input: inputs/script_1.txt")
        print("  Output: outputs/script_1_presentation.*")
        sys.exit(1)

    input_filename = sys.argv[1]

    # Setup directories
    setup_directories()

    # Setup paths
    input_path = Path("inputs") / input_filename
    base_name = Path(input_filename).stem

    # Parse arguments
    content_type = "business"
    output_format = "txt"
    theme = "default"

    for i, arg in enumerate(sys.argv):
        if arg == "--type" and i + 1 < len(sys.argv):
            content_type = sys.argv[i + 1]
        elif arg == "--format" and i + 1 < len(sys.argv):
            output_format = sys.argv[i + 1]
        elif arg == "--theme" and i + 1 < len(sys.argv):
            theme = sys.argv[i + 1]

    # Check input file
    if not input_path.exists():
        print(f"❌ Error: File '{input_path}' not found")
        print(f"💡 Make sure to place your input file in the inputs/ directory")
        print(f"📁 Expected location: {input_path}")
        sys.exit(1)

    # Check API key for OpenAI
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        print("Set it with: export OPENAI_API_KEY='your-api-key'")
        sys.exit(1)

    script_dir = Path(__file__).parent

    # Define output paths
    cleaned_file = Path("outputs") / f"{base_name}_cleaned.txt"
    slides_file = Path("outputs") / f"{base_name}_comprehensive_script.txt"

    print(f"\n🐛 DEBUG: File paths:")
    print(f"   Input: {input_path}")
    print(f"   Cleaned: {cleaned_file}")
    print(f"   Slides: {slides_file}")
    print(f"   Format: {output_format}")

    # Step 1: Clean and prepare content
    print(f"\n📍 STEP 1: Preparing content")
    if not run_command([
        "python3", str(script_dir / "prepare_content.py"),
        str(input_path), str(cleaned_file)
    ], "Cleaning and preparing content"):
        sys.exit(1)

    # Step 2: Generate slides with AI
    print(f"\n📍 STEP 2: Generating slides with AI")
    if not run_command([
        "python3", str(script_dir / "generate_slides.py"),
        input_filename, "--type", content_type
    ], f"Generating comprehensive slides ({content_type} format)"):
        sys.exit(1)

    print(f"\n📍 STEP 3: Processing output format ({output_format})")

    # Step 3: Convert to final format
    if output_format == "marp":
        final_file = Path("outputs") / f"{base_name}_presentation.md"
        if not run_command([
            "python3", str(script_dir / ".." / "utils" /
                           "exporters" / "marp_generator.py"),
            str(slides_file), str(final_file), theme
        ], f"Converting to Marp ({theme} theme)"):
            sys.exit(1)

        print(f"\n✅ Complete! Your presentation is ready:")
        print(f"📄 Marp file: {final_file}")
        print(f"\n🎯 Next steps:")
        print(f"  1. Review slides: {final_file}")
        print(
            f"  2. Generate PDF: marp {final_file} -o outputs/{base_name}.pdf")

    elif output_format == "json":
        # Convert slides to JSON structure
        json_file = Path("outputs") / f"{base_name}_slides.json"
        print(f"🔄 Converting to JSON format...")

        try:
            with open(slides_file, 'r') as f:
                content = f.read()

            # Simple JSON structure
            import json
            import re

            slides = []
            # Skip first empty part
            slide_blocks = re.split(r'SLIDE \d+:', content)[1:]

            for i, block in enumerate(slide_blocks, 1):
                lines = block.strip().split('\n')
                title = lines[0].strip() if lines else f"Slide {i}"

                slide_data = {
                    "slide_number": i,
                    "title": title,
                    "content": block.strip()
                }
                slides.append(slide_data)

            with open(json_file, 'w') as f:
                json.dump(
                    {"slides": slides, "total_slides": len(slides)}, f, indent=2)

            print(f"✅ JSON generated: {json_file}")
            final_file = json_file

        except Exception as e:
            print(f"❌ Error generating JSON: {e}")
            sys.exit(1)

    else:  # txt format
        final_file = Path("outputs") / f"{base_name}_comprehensive_script.txt"
        print(f"\n✅ Complete! Your comprehensive slide script is ready:")
        print(f"📄 Text file: {final_file}")

    # Summary
    print(f"\n📊 WORKFLOW SUMMARY:")
    print(f"{'='*60}")
    print(f"📥 Input: {input_path}")
    print(f"🧹 Cleaned: {cleaned_file}")
    print(f"🎯 Content type: {content_type}")
    print(f"📤 Output format: {output_format}")
    print(f"📄 Final output: {final_file}")
    print(f"📁 All files saved to: outputs/")
    print(f"{'='*60}")

    # Cleanup intermediate files option
    print(f"\n🗑️  Cleanup intermediate files? (y/n): ", end="")
    response = input().strip().lower()
    if response == 'y':
        try:
            if cleaned_file.exists():
                os.remove(cleaned_file)
            if output_format != "txt" and slides_file.exists():
                os.remove(slides_file)
            print("✅ Intermediate files cleaned up")
        except Exception as e:
            print(f"⚠️  Warning: Could not remove some files: {e}")


if __name__ == "__main__":
    main()
