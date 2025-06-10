#!/usr/bin/env python3
"""
Example: Complete Intelligence-to-Deck workflow with Google Slides integration.
Demonstrates the full pipeline from content to Google Slides presentation.
"""

import os
import sys
from pathlib import Path


def setup_example():
    """Create example content and check prerequisites."""

    print("🎯 Setting up Intelligence-to-Deck Google Slides Example")
    print("="*60)

    # Create sample content
    sample_content = """Digital Transformation in Modern Business

Introduction to Digital Innovation
Digital transformation represents a fundamental shift in how businesses operate, leveraging technology to improve processes, enhance customer experiences, and drive competitive advantage. Organizations across all industries are embracing digital technologies to modernize their operations and create new value propositions.

Current Technology Landscape
• Cloud computing adoption accelerating
• AI and machine learning integration expanding
• Mobile-first strategies becoming standard
• Data analytics driving decision-making
• Automation transforming workflows
• Cybersecurity concerns increasing

Strategic Benefits of Digital Transformation
• Enhanced operational efficiency
• Improved customer engagement
• Data-driven decision making
• Increased agility and scalability
• Cost reduction through automation
• New revenue stream opportunities
• Better employee productivity
• Competitive market positioning

Implementation Challenges
• Legacy system integration complexity
• Skills gap in digital technologies
• Change management resistance
• Budget constraints and ROI concerns
• Data privacy and security issues
• Vendor selection difficulties
• Timeline and resource planning
• Organizational culture adaptation

Key Success Factors
• Leadership commitment and vision
• Clear strategic roadmap
• Employee training and development
• Robust data governance
• Agile implementation approach
• Continuous monitoring and optimization
• Partner ecosystem development
• Customer-centric focus

Measuring Success and ROI
• 30% increase in operational efficiency
• 25% improvement in customer satisfaction
• 40% reduction in manual processes
• 20% growth in digital revenue streams
• Enhanced data accuracy and insights
• Faster time-to-market for products
• Improved employee engagement
• Stronger competitive positioning

Future Outlook and Recommendations
Organizations should adopt a holistic approach to digital transformation, focusing on people, processes, and technology. Success requires strong leadership, clear vision, and commitment to continuous innovation and adaptation in an ever-evolving digital landscape."""

    # Create directories
    inputs_dir = Path("inputs")
    inputs_dir.mkdir(exist_ok=True)

    # Write sample content
    sample_file = inputs_dir / "digital_transformation.txt"
    with open(sample_file, 'w') as f:
        f.write(sample_content)

    print(f"✅ Created sample content: {sample_file}")

    # Check prerequisites
    print("\n🔍 Checking Prerequisites:")

    # Check OpenAI API key
    if os.getenv('OPENAI_API_KEY'):
        print("✅ OpenAI API key configured")
    else:
        print("❌ OpenAI API key missing")
        print("   Set with: export OPENAI_API_KEY='your-key'")
        return False

    # Check Google Slides credentials
    credentials_file = Path("credentials.json")
    if credentials_file.exists():
        print("✅ Google Slides credentials found")
    else:
        print("❌ Google Slides credentials missing:")
        print("   1. Enable Google Slides API in Google Cloud Console")
        print("   2. Create OAuth 2.0 credentials")
        print("   3. Download as credentials.json")
        print("   Setup guide: https://developers.google.com/slides/api/quickstart/python")
        return False

    return True


def run_workflow():
    """Run the complete workflow."""

    print("\n🚀 Running Complete Workflow:")
    print("="*40)

    # Import after checking prerequisites
    import subprocess

    # Run the full workflow
    cmd = [
        "python3", "src/v2/full_workflow.py",
        "digital_transformation.txt",
        "--type", "business",
        "--format", "slides",
        "--title", "Digital Transformation Strategy"
    ]

    print(f"📝 Command: {' '.join(cmd)}")

    try:
        result = subprocess.run(
            cmd, check=True, capture_output=True, text=True)

        print("✅ Workflow completed successfully!")
        print("\n📄 Google Slides presentation created!")

        # Extract presentation URL from output if available
        output_lines = result.stdout.split('\n')
        for line in output_lines:
            if 'Presentation URL:' in line or 'View at:' in line:
                print(f"🔗 {line}")

        # Show other outputs
        outputs_dir = Path("outputs")
        if outputs_dir.exists():
            print(f"\n📁 Generated files in outputs/:")
            for file in outputs_dir.glob("digital_transformation*"):
                size = file.stat().st_size
                print(f"   📄 {file.name} ({size:,} bytes)")

        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Workflow failed: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False


def demo_google_slides_features():
    """Demonstrate key Google Slides integration features."""

    print("\n🎯 Google Slides Integration Features:")
    print("="*45)

    features = [
        "✅ Real-time collaborative editing",
        "✅ Cloud-based access from any device",
        "✅ Automatic version history",
        "✅ Link-based sharing with permissions",
        "✅ Comment and suggestion system",
        "✅ Integration with Google Workspace",
        "✅ Mobile editing capabilities",
        "✅ Professional slide layouts",
        "✅ Export to PDF/PowerPoint options",
        "✅ Free API with generous quotas"
    ]

    for feature in features:
        print(f"  {feature}")

    print("\n🔧 Setup Requirements:")
    print("  1. Google Account")
    print("  2. Google Cloud Project")
    print("  3. Google Slides API enabled")
    print("  4. OAuth 2.0 credentials downloaded")

    print("\n📋 Workflow Steps:")
    print("  1. Content preparation and cleaning")
    print("  2. AI-powered slide generation")
    print("  3. Google Slides API integration")
    print("  4. Shareable presentation creation")


def main():
    """Main example function."""

    print("🎯 Intelligence-to-Deck Google Slides Integration Example")
    print("This example demonstrates the complete workflow from content to Google Slides")
    print()

    # Demo features first
    demo_google_slides_features()

    # Setup
    print("\n" + "="*60)
    if not setup_example():
        print("\n❌ Prerequisites not met. Please configure credentials and try again.")
        print("\n📚 Setup Guide:")
        print("1. Get OpenAI API key: https://platform.openai.com/api-keys")
        print("2. Enable Google Slides API: https://console.cloud.google.com/")
        print("3. Download credentials.json from Google Cloud Console")
        sys.exit(1)

    # Confirm with user
    print("\n⚡ Ready to run the complete workflow!")
    print("This will:")
    print("  1. Process the sample content")
    print("  2. Generate AI slides (business format)")
    print("  3. Create Google Slides presentation")
    print("  4. Provide shareable link")
    print()

    confirm = input("Continue? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Cancelled.")
        sys.exit(0)

    # Run workflow
    if run_workflow():
        print("\n🎉 Example completed successfully!")
        print("\nNext steps:")
        print("  1. Open the Google Slides link provided above")
        print("  2. Share with collaborators for real-time editing")
        print("  3. Customize styling and add images")
        print("  4. Try with your own content in inputs/")
        print("\n💡 Tips:")
        print("  • Use --title to customize presentation titles")
        print("  • Try different --type options (business, technical)")
        print("  • Generated presentations are automatically saved to your Google Drive")
    else:
        print("\n❌ Example failed. Check error messages above.")
        print("\n🔧 Troubleshooting:")
        print("  • Verify credentials.json file is valid")
        print("  • Check Google Slides API is enabled")
        print("  • Ensure OpenAI API key is correct")
        print("  • Check internet connectivity")
        sys.exit(1)


if __name__ == "__main__":
    main()
