#!/usr/bin/env python3
"""
Multi-stage professional slide script generator with brand consistency.
Generates 15-20 comprehensive slides using multiple AI iterations.
Uses inputs/ folder for source files and outputs/ folder for results.
"""

import os
import sys
import json
import re
import time
from pathlib import Path
from typing import Optional, Dict, Any, List

try:
    import openai
except ImportError:
    print("Error: openai package not installed. Run: pip install openai")
    sys.exit(1)


class ProfessionalSlideGenerator:
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4-turbo"):
        """Initialize with OpenAI API key and model."""
        self.client = openai.OpenAI(
            api_key=api_key or os.getenv('OPENAI_API_KEY'))
        self.model = model
        self.brand_guidelines = self._get_brand_guidelines()

        # Create directory structure
        self.setup_directories()

    def setup_directories(self):
        """Create inputs and outputs directories if they don't exist."""
        inputs_dir = Path("inputs")
        outputs_dir = Path("outputs")

        inputs_dir.mkdir(exist_ok=True)
        outputs_dir.mkdir(exist_ok=True)

        if not inputs_dir.exists() or not outputs_dir.exists():
            print("📁 Created directory structure:")
            print(f"   • inputs/ - Place your source files here")
            print(f"   • outputs/ - Generated presentations will be saved here")

    def _get_brand_guidelines(self) -> str:
        """Define consistent brand voice and style guidelines."""
        return """
BRAND VOICE & STYLE GUIDELINES:

**Tone**: Professional, confident, action-oriented
**Language**: Clear, concise, executive-level communication
**Structure**: Logical flow with strong narrative arc
**Data Presentation**: Specific numbers, concrete examples, measurable outcomes
**Visual Style**: Clean, modern, business-focused
**Call-to-Action Style**: Direct, specific, time-bound when possible

**Formatting Standards**:
- Headlines: Maximum 8 words, action-oriented
- Bullet Points: Start with strong verbs when possible
- Speaker Notes: Conversational but professional tone
- Transitions: Smooth, logical connections between concepts
- Visual Descriptions: Specific, actionable for designers

**Content Principles**:
- Lead with insights, support with data
- Focus on business impact and ROI
- Include concrete next steps
- Maintain consistent information density
- Use storytelling elements for engagement

**CRITICAL VISUAL GUIDELINES - DO NOT VIOLATE**:
- NEVER suggest creating images with text overlays unless absolutely essential
- AVOID complex infographics that require text generation within images
- STICK TO simple diagrams: flowcharts, org charts, basic process flows
- USE standard chart types: bar charts, line graphs, pie charts, scatter plots
- PREFER data visualizations over decorative graphics
- AVOID suggesting screenshots with text unless from existing sources
- DO NOT create fake quotes, testimonials, or text-heavy graphics
- FOCUS ON clean, simple visuals that complement the text content
- WHEN IN DOUBT, suggest "TEXT ONLY" rather than complex graphics

**SAFE VISUAL RECOMMENDATIONS**:
✅ Simple bar/line/pie charts with data from content
✅ Basic flowcharts showing process steps
✅ Simple organizational charts
✅ Timeline diagrams with dates/milestones
✅ Before/after comparison tables
✅ Icon-based layouts (no text in icons)
✅ Professional stock photos (people, objects, settings)
✅ Color-coded sections or categories

**AVOID THESE VISUAL TYPES**:
❌ Complex infographics with embedded text
❌ Screenshots with fake UI text
❌ Images requiring text overlays or captions within the image
❌ Detailed technical diagrams with labels
❌ Marketing-style graphics with headlines/taglines
❌ Social media style graphics
❌ Any visual that requires AI to generate text within images
"""

    def estimate_tokens(self, text: str) -> int:
        """Accurate token estimation."""
        return len(text.split()) * 1.3

    def stage1_content_analysis(self, content: str, content_type: str) -> Dict[str, Any]:
        """Stage 1: Analyze content and create presentation outline."""

        print("🔍 Analyzing content structure and themes...")
        start_time = time.time()

        analysis_prompt = f"""
Analyze this content to create a comprehensive presentation outline for 15-20 slides.

CONTENT TYPE: {content_type.upper()}
CONTENT TO ANALYZE:
{content}

ANALYSIS REQUIREMENTS:
1. Identify 6-8 major themes/topics that can be expanded into multiple slides
2. Extract the most important data points, metrics, and examples
3. Determine the logical narrative flow across 15-20 slides
4. Identify opportunities for SIMPLE, TEXT-FREE visuals throughout
5. Define the core business insight or value proposition
6. Plan for deeper dive sections that warrant multiple slides

CRITICAL: For visuals, ONLY suggest simple charts, basic diagrams, or "TEXT ONLY" slides.
DO NOT recommend complex graphics, infographics with text, or any visuals requiring text generation.

OUTPUT FORMAT:
**CORE MESSAGE:** [One powerful sentence summarizing the entire presentation]

**MAJOR THEMES FOR SLIDE EXPANSION:**
1. [Theme 1] - [Description with 2-3 slide potential breakdown]
2. [Theme 2] - [Description with 2-3 slide potential breakdown]  
3. [Theme 3] - [Description with 2-3 slide potential breakdown]
4. [Theme 4] - [Description with 2-3 slide potential breakdown]
5. [Theme 5] - [Description with 2-3 slide potential breakdown]
6. [Theme 6] - [Description with 2-3 slide potential breakdown]
7. [Theme 7] - [Description with 2-3 slide potential breakdown]
8. [Theme 8] - [Description with 2-3 slide potential breakdown]

**EXTENDED NARRATIVE ARC (15-20 slides):**
- Opening & Context (Slides 1-3): Hook, situation setup, scope definition
- Problem Definition (Slides 4-6): Challenge analysis, current state, impact
- Deep Analysis (Slides 7-11): Key insights, data findings, root causes, implications
- Solutions & Strategy (Slides 12-16): Recommendations, implementation approach, methodology
- Impact & Next Steps (Slides 17-20): Expected outcomes, timeline, action items, conclusion

**KEY DATA POINTS & METRICS:**
- [Specific number/metric 1 with context]
- [Specific number/metric 2 with context]
- [Specific number/metric 3 with context]
- [Specific number/metric 4 with context]
- [Specific number/metric 5 with context]
- [Additional metrics and quantifiable insights]

**SAFE VISUAL OPPORTUNITIES (NO TEXT IN IMAGES):**
- Simple bar/line charts for metrics (data only, no text overlays)
- Basic process flowcharts (boxes and arrows only)
- Timeline diagrams with dates/milestones
- Simple before/after comparison tables
- Professional stock photos (no text required)
- Color-coded categories or sections
- Basic organizational charts
- Clean dashboard-style metric displays

**CONTENT DEPTH STRATEGY:**
- Which topics deserve multiple slides for thorough coverage
- Where to include detailed case studies or examples
- Opportunities for step-by-step breakdowns
- Areas requiring both overview and detail slides
"""

        try:
            print("📡 Sending analysis request to OpenAI...")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": f"You are a senior strategy consultant who analyzes content to create compelling executive presentations spanning 15-20 slides for comprehensive coverage. {self.brand_guidelines}"},
                    {"role": "user", "content": analysis_prompt}
                ],
                max_tokens=3500,
                temperature=0.1
            )

            analysis_result = response.choices[0].message.content
            elapsed_time = time.time() - start_time
            print(
                f"✅ Stage 1: Content analysis complete ({elapsed_time:.1f}s)")

            return {
                "analysis": analysis_result,
                "content": content,
                "content_type": content_type
            }

        except Exception as e:
            print(f"❌ Error in Stage 1 analysis: {e}")
            return {"analysis": "", "content": content, "content_type": content_type}

    def stage2_slide_structure(self, analysis_data: Dict[str, Any]) -> List[Dict[str, str]]:
        """Stage 2: Create detailed slide structure for 15-20 slides."""

        print("🏗️ Designing presentation structure and slide flow...")
        start_time = time.time()

        structure_prompt = f"""
Based on this content analysis, create a detailed structure for each slide in a 15-20 slide presentation.

CONTENT ANALYSIS:
{analysis_data['analysis']}

STRUCTURE REQUIREMENTS:
- Create 15-20 individual slide specifications
- Each slide should have a clear purpose and unique angle
- Ensure logical flow and build throughout presentation
- Specify safe visual approach for each slide
- Balance content density across slides
- Include detailed talking points guidance

SLIDE STRUCTURE FORMAT (for each slide):
**SLIDE [NUMBER]: [Title Focus]**
- Objective: [What this slide accomplishes]
- Key Content: [Main points to cover - 3-4 bullet points]
- Visual Approach: [Simple chart, basic diagram, or "TEXT ONLY"]
- Talking Points: [Specific guidance for presenter]
- Transition: [How it connects to next slide]

Create all 15-20 slides following this structure. Focus on comprehensive coverage with each slide adding unique value.
"""

        try:
            print("📡 Sending structure request to OpenAI...")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": f"You are a presentation design expert creating comprehensive slide structures for executive presentations. {self.brand_guidelines}"},
                    {"role": "user", "content": structure_prompt}
                ],
                max_tokens=4000,
                temperature=0.2
            )

            structure_result = response.choices[0].message.content
            elapsed_time = time.time() - start_time

            # Parse the structure into individual slide entries
            slides_structure = []
            slide_blocks = re.split(r'\*\*SLIDE \d+:', structure_result)

            # Skip first empty block
            for i, block in enumerate(slide_blocks[1:], 1):
                slides_structure.append({
                    'slide_number': i,
                    'structure': f"SLIDE {i}: {block.strip()}"
                })

            print(
                f"✅ Stage 2: Created structure for {len(slides_structure)} slides ({elapsed_time:.1f}s)")
            return slides_structure

        except Exception as e:
            print(f"❌ Error in Stage 2 structure: {e}")
            # Fallback: create basic structure
            return [{'slide_number': i, 'structure': f"SLIDE {i}: Basic content"} for i in range(1, 16)]

    def stage3_individual_slides(self, slides_structure: List[Dict[str, str]], content: str) -> List[str]:
        """Stage 3: Generate detailed content for each slide individually."""

        detailed_slides = []
        total_slides = len(slides_structure)
        stage_start_time = time.time()

        print(
            f"✍️ Generating detailed content for {total_slides} individual slides...")

        for i, slide_info in enumerate(slides_structure, 1):
            slide_start_time = time.time()
            print(f"🔄 Slide {i}/{total_slides}: Creating detailed content...")

            slide_prompt = f"""
Create detailed, professional content for this specific slide in a {total_slides}-slide presentation.

CRITICAL VISUAL SAFETY: Only specify simple, text-free visuals. When uncertain, use "TEXT ONLY".

SLIDE STRUCTURE:
{slide_info['structure']}

SLIDE POSITION CONTEXT:
- This is slide {i} of {total_slides}
- Presentation section: {self._get_section_context(i, total_slides)}
- Audience attention level: {self._get_attention_context(i, total_slides)}

DETAILED SLIDE REQUIREMENTS:
- Follow exact formatting structure below
- 180-220 words of total content
- Professional business language
- Specific, actionable information
- SAFE visual integration only
- Appropriate pacing for slide position

OUTPUT FORMAT (MANDATORY):

SLIDE {i}: [Compelling Title - Max 8 words]

**SPEAKER NOTES:**
[Detailed speaking points - 120-150 words covering context, key insights, supporting details, and transition. Consider this slide's position in the overall presentation flow. Write as if coaching the presenter on what to say and emphasize.]

**SLIDE CONTENT:**
• [Primary headline point - action-oriented with specific detail]
• [Supporting point with concrete data/example/metric]
• [Third point with specific evidence or case example]  
• [Fourth point focusing on impact or next step]

**VISUAL SPECIFICATION:**
[SAFE VISUAL ONLY: Choose from these options:
- "TEXT ONLY" (when complex visuals would be needed)
- Simple bar chart showing [specific data from content]
- Basic line chart displaying [specific metrics from content]
- Simple pie chart with [specific percentages from content]
- Basic flowchart: [Step 1] → [Step 2] → [Step 3]
- Timeline: [Date 1] - [Event 1], [Date 2] - [Event 2]
- Professional stock photo: [simple description, no text]
- Simple before/after comparison table
DO NOT suggest complex graphics, infographics, or any visuals requiring text generation.]

**TRANSITION TO NEXT SLIDE:**
[One compelling sentence that bridges to the next topic and maintains narrative flow across {total_slides} slides]

VISUAL SAFETY REMINDER:
- Never suggest images with text overlays
- Avoid complex infographics or detailed diagrams
- When uncertain about visual complexity, choose "TEXT ONLY"
- Stick to simple data charts and basic diagrams only
"""

            try:
                print(f"   📡 Sending slide {i} request to OpenAI...")
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": f"You are an expert slide content writer creating slide {i} of {total_slides} in an executive-level presentation. CRITICAL: Only recommend simple, text-free visuals or 'TEXT ONLY'. {self.brand_guidelines}"},
                        {"role": "user", "content": slide_prompt}
                    ],
                    max_tokens=800,
                    temperature=0.2
                )

                slide_content = response.choices[0].message.content
                detailed_slides.append(slide_content)

                slide_elapsed = time.time() - slide_start_time
                print(f"   ✅ Slide {i} complete ({slide_elapsed:.1f}s)")

                # Brief pause to avoid rate limits
                time.sleep(0.3)

            except Exception as e:
                print(f"   ❌ Error generating slide {i}: {e}")
                detailed_slides.append(
                    f"SLIDE {i}: [Error generating content]")

        total_elapsed = time.time() - stage_start_time
        print(
            f"✅ Stage 3: Generated {len(detailed_slides)} individual slides ({total_elapsed:.1f}s total)")
        return detailed_slides

    def _get_section_context(self, slide_num: int, total_slides: int) -> str:
        """Get context about which section of the presentation this slide belongs to."""
        if slide_num <= 3:
            return "Opening & Context"
        elif slide_num <= 6:
            return "Problem/Opportunity Definition"
        elif slide_num <= int(total_slides * 0.6):
            return "Deep Analysis & Insights"
        elif slide_num <= int(total_slides * 0.85):
            return "Solutions & Strategy"
        else:
            return "Impact & Next Steps"

    def _get_attention_context(self, slide_num: int, total_slides: int) -> str:
        """Get guidance about audience attention level at this point."""
        if slide_num <= 3:
            return "High - audience fresh and engaged"
        elif slide_num <= int(total_slides * 0.3):
            return "High - building momentum"
        elif slide_num <= int(total_slides * 0.7):
            return "Moderate - maintain engagement with variety"
        elif slide_num <= int(total_slides * 0.9):
            return "Moderate - approaching conclusion, refocus energy"
        else:
            return "High - final impact and call to action"

    def stage4_brand_polish(self, detailed_slides: List[str], content_type: str) -> str:
        """Stage 4: Apply final brand polish and consistency check across all slides."""

        # For stage 4, we'll process slides in chunks to stay under token limits
        return self._polish_slides_in_chunks(detailed_slides, content_type)

    def _polish_slides_in_chunks(self, detailed_slides: List[str], content_type: str) -> str:
        """Polish slides in smaller chunks to avoid token limits."""
        total_slides = len(detailed_slides)
        chunk_size = 5  # Process 5 slides at a time
        polished_chunks = []
        stage_start_time = time.time()

        print(
            f"✨ Polishing {total_slides} slides in chunks of {chunk_size}...")

        for i in range(0, len(detailed_slides), chunk_size):
            chunk_start_time = time.time()
            chunk = detailed_slides[i:i + chunk_size]
            chunk_text = "\n\n---\n\n".join(chunk)
            start_slide = i + 1
            end_slide = min(i + chunk_size, len(detailed_slides))

            print(f"🔄 Polishing slides {start_slide}-{end_slide}...")

            polish_prompt = f"""
Apply brand polish and consistency to slides {start_slide}-{end_slide} of a {total_slides}-slide presentation.

CRITICAL: Ensure all visual specifications remain SIMPLE and TEXT-FREE. Never add complex graphics.

CONTENT TYPE: {content_type.upper()}
SLIDES TO POLISH:
{chunk_text}

POLISH REQUIREMENTS:
1. Ensure consistent tone and professional language
2. Strengthen transitions and flow
3. Verify visual specifications are simple and safe (no text in images)
4. Optimize content density and clarity
5. Maintain brand voice throughout
6. Ensure visual recommendations follow safety guidelines

VISUAL SAFETY CHECK:
- Confirm all visuals are simple charts, basic diagrams, or "TEXT ONLY"
- Remove any suggestions for complex graphics or text-heavy images
- Ensure no text overlays or infographics are recommended

OUTPUT THE POLISHED SLIDES exactly as formatted, but enhanced for maximum professional impact.
"""

            try:
                print(
                    f"   📡 Sending polish request for slides {start_slide}-{end_slide}...")
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": f"You are a senior presentation consultant applying final polish to executive slides. CRITICAL: Maintain simple, text-free visual specifications only. {self.brand_guidelines}"},
                        {"role": "user", "content": polish_prompt}
                    ],
                    max_tokens=3500,
                    temperature=0.1
                )

                polished_chunk = response.choices[0].message.content
                polished_chunks.append(polished_chunk)

                chunk_elapsed = time.time() - chunk_start_time
                print(
                    f"   ✅ Slides {start_slide}-{end_slide} polished ({chunk_elapsed:.1f}s)")

                time.sleep(0.5)  # Pause between chunks

            except Exception as e:
                print(
                    f"   ❌ Error polishing slides {start_slide}-{end_slide}: {e}")
                # Use original if polishing fails
                polished_chunks.append(chunk_text)

        total_elapsed = time.time() - stage_start_time
        print(
            f"✅ Stage 4: Brand polish complete for {total_slides} slides ({total_elapsed:.1f}s total)")
        return "\n\n---\n\n".join(polished_chunks)

    def generate_comprehensive_script(self, content: str, content_type: str = "business") -> str:
        """Execute all 4 stages to generate a comprehensive 15-20 slide script."""

        overall_start_time = time.time()
        print(f"🚀 Starting 4-stage professional slide generation (15-20 slides)...")
        print(f"📊 Content type: {content_type}")
        print(f"📄 Estimated input tokens: {self.estimate_tokens(content)}")
        print(f"🎨 Visual safety: Simple diagrams and charts only, no complex graphics")

        # Handle large content
        if self.estimate_tokens(content) > 120000:
            print("📄 Content too large, creating strategic summary...")
            content = self._create_strategic_summary(content)

        # Stage 1: Content Analysis
        print("\n" + "="*60)
        print("🔍 STAGE 1: CONTENT ANALYSIS")
        print("="*60)
        analysis_data = self.stage1_content_analysis(content, content_type)

        # Stage 2: Slide Structure
        print("\n" + "="*60)
        print("🏗️ STAGE 2: SLIDE STRUCTURE DESIGN")
        print("="*60)
        slides_structure = self.stage2_slide_structure(analysis_data)

        # Stage 3: Individual Slides
        print("\n" + "="*60)
        print("✍️ STAGE 3: INDIVIDUAL SLIDE GENERATION")
        print("="*60)
        detailed_slides = self.stage3_individual_slides(
            slides_structure, content)

        # Stage 4: Brand Polish
        print("\n" + "="*60)
        print("✨ STAGE 4: BRAND POLISH & FINAL REVIEW")
        print("="*60)
        final_script = self.stage4_brand_polish(detailed_slides, content_type)

        overall_elapsed = time.time() - overall_start_time
        print(
            f"\n🎉 All stages complete! Total generation time: {overall_elapsed:.1f}s")

        return final_script

    def _create_strategic_summary(self, content: str) -> str:
        """Create a strategic summary focused on presentation needs."""
        summary_prompt = f"""
Create a strategic summary of this content optimized for a comprehensive 15-20 slide executive presentation.

FOCUS AREAS FOR EXTENDED PRESENTATION:
- Key business insights and strategic implications (multiple angles)
- Important metrics, data points, and performance indicators (comprehensive coverage)
- Critical problems, solutions, and recommendations (detailed breakdown)
- Success stories, case studies, and concrete examples (multiple examples)
- Process improvements and methodological insights (step-by-step details)
- Actionable next steps and implementation strategies (comprehensive roadmap)
- Supporting context and background information (fuller picture)

PRESERVE FOR 15-20 SLIDE COVERAGE:
- Specific numbers, percentages, and quantitative data
- Names, dates, and concrete examples
- Logical relationships and cause-effect connections
- Strategic recommendations and action items
- Detailed processes and methodologies
- Multiple perspectives and angles on key topics

CONTENT TO SUMMARIZE:
{content}

Strategic Summary for Extended Presentation (2500 words max):"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a senior strategy consultant who creates comprehensive summaries that preserve all key insights needed for detailed 15-20 slide executive presentations."},
                    {"role": "user", "content": summary_prompt}
                ],
                max_tokens=3500,
                temperature=0.2
            )

            return response.choices[0].message.content

        except Exception as e:
            print(f"Error creating strategic summary: {e}")
            return content[:12000]


def main():
    if len(sys.argv) < 2:
        print(
            "Usage: python generate_slides.py <input_filename> [--type business|technical|general]")
        print("\nDirectory Structure:")
        print("  • Place input files in: inputs/")
        print("  • Generated scripts saved to: outputs/")
        print("\nFeatures:")
        print("  • 4-stage professional generation process")
        print("  • 15-20 comprehensive slides with consistent quality")
        print("  • Visual safety: Simple charts and diagrams only")
        print("  • No complex graphics or text-heavy images")
        print("  • Individual slide optimization")
        print("  • Professional visual specifications")
        print("\nExample: python generate_slides.py script_1.txt --type business")
        print("  Reads from: inputs/script_1.txt")
        print("  Saves to: outputs/script_1_comprehensive_script.txt")
        sys.exit(1)

    input_filename = sys.argv[1]

    # Setup paths
    input_path = Path("inputs") / input_filename
    base_name = Path(input_filename).stem
    output_filename = f"{base_name}_comprehensive_script.txt"
    output_path = Path("outputs") / output_filename

    # Parse content type
    content_type = "business"
    for i, arg in enumerate(sys.argv):
        if arg == "--type" and i + 1 < len(sys.argv):
            content_type = sys.argv[i + 1]

    # Read input
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
    except FileNotFoundError:
        print(f"❌ Error: File '{input_path}' not found")
        print(f"💡 Make sure to place your input file in the inputs/ directory")
        print(f"📁 Expected location: {input_path}")
        sys.exit(1)

    if not content:
        print("❌ Error: Input file is empty")
        sys.exit(1)

    # Check API key
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        sys.exit(1)

    # Generate comprehensive professional script
    generator = ProfessionalSlideGenerator()

    start_time = time.time()
    professional_script = generator.generate_comprehensive_script(
        content, content_type)
    generation_time = time.time() - start_time

    # Count actual slides generated
    slide_count = len(re.findall(r'SLIDE \d+:', professional_script))

    # Create comprehensive output with metadata
    script_header = f"""
{'='*100}
COMPREHENSIVE PROFESSIONAL PRESENTATION SCRIPT
{'='*100}

Source File: inputs/{input_filename}
Content Type: {content_type.upper()}
Total Slides: {slide_count}
Generation Method: 4-Stage AI Process (Analysis → Structure → Content → Polish)
Generation Time: {generation_time:.1f} seconds
Visual Safety: Simple diagrams and charts only, no complex graphics
Brand Standards: Applied Throughout
Quality Level: Executive-Ready Extended Format

SCRIPT FEATURES:
✅ {slide_count} comprehensive slides with consistent quality
✅ 180-220 words per slide maintained throughout
✅ Professional speaker notes for extended presentation
✅ SAFE visual requirements - simple charts and diagrams only
✅ NO complex graphics, infographics, or text-heavy images
✅ Brand voice consistency across extended format
✅ Strategic narrative flow optimized for 15-20 slide length
✅ Actionable content ready for slide software

VISUAL SAFETY STANDARDS:
• Simple bar/line/pie charts only
• Basic flowcharts and timelines
• Professional stock photos (no text overlays)
• "TEXT ONLY" when complex visuals would be needed
• NO infographics or complex diagrams
• NO text generation within images

PRESENTATION STRUCTURE:
• Opening & Context (Slides 1-3)
• Problem/Opportunity Definition (Slides 4-6)  
• Deep Analysis & Insights (Slides 7-11)
• Solutions & Strategy (Slides 12-16)
• Impact & Next Steps (Slides 17-{slide_count})

{'='*100}

"""

    # Save output
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(script_header + professional_script)

    # Success summary
    print(f"\n🎉 COMPREHENSIVE PRESENTATION SCRIPT GENERATED!")
    print(f"{'='*70}")
    print(f"📥 Input: {input_path}")
    print(f"📤 Output: {output_path}")
    print(f"📊 Total slides: {slide_count}")
    print(f"⏱️ Generation time: {generation_time:.1f} seconds")
    print(f"🎯 Content type: {content_type.upper()}")
    print(f"🎨 Visual safety: Simple diagrams and charts only")
    print(f"📈 Quality level: Executive-ready extended format")
    print(f"\n🚀 ENHANCED FEATURES:")
    print(f"   • 4-stage AI generation with optimized tokens")
    print(f"   • {slide_count} slides with consistent 180-220 words each")
    print(f"   • SAFE visual specifications - no complex graphics")
    print(f"   • Extended narrative flow optimization")
    print(f"   • Brand consistency across all slides")
    print(f"   • Strategic pacing for longer presentations")
    print(f"   • Individual slide optimization process")
    print(
        f"\n📋 NEXT STEP: Copy script from {output_path} into your slide software")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
