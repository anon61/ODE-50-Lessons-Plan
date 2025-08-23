#!/usr/bin/env python3
"""
Process ODE Lessons 19-50 from raw text files into structured lesson format
"""

import os
import re
import subprocess
from pathlib import Path

def extract_lesson_components(filepath):
    """Extract the three components from a lesson file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Initialize components
    audio_script = ""
    theory_latex = ""
    problems_latex = ""
    
    # Try to find audio script (Part 1, Component 1, or before first latex block)
    audio_match = re.search(r'(Component 1:|Part 1:)(.*?)```latex', content, re.DOTALL)
    if audio_match:
        audio_script = audio_match.group(2).strip()
    else:
        # Try to get content before first latex block
        first_latex = content.find('```latex')
        if first_latex > 0:
            audio_script = content[:first_latex].strip()
            # Remove the lesson title if present
            audio_script = re.sub(r'^#.*?\n+', '', audio_script)
    
    # Find LaTeX blocks
    latex_blocks = re.findall(r'```latex(.*?)```', content, re.DOTALL)
    
    if len(latex_blocks) >= 2:
        theory_latex = latex_blocks[0].strip()
        problems_latex = latex_blocks[1].strip()
    elif len(latex_blocks) == 1:
        # Sometimes theory and problems might be in one block
        theory_latex = latex_blocks[0].strip()
        # Try to split at common section marker
        if '\\title{Practice Problems' in theory_latex:
            parts = theory_latex.split('\\begin{document}', 1)
            if len(parts) == 2:
                theory_part = parts[0] + '\\begin{document}\n' + parts[1].split('\\title{Practice Problems')[0]
                problems_part = '\\documentclass' + parts[1].split('\\documentclass', 1)[-1] if '\\documentclass' in parts[1] else ''
                if problems_part:
                    theory_latex = theory_part
                    problems_latex = problems_part
    
    # Clean up audio script - remove markdown headers
    audio_script = re.sub(r'^#+\s+.*$', '', audio_script, flags=re.MULTILINE)
    audio_script = audio_script.strip()
    
    # Add Episode header if missing
    lesson_num = int(Path(filepath).stem)
    if not audio_script.startswith('Episode'):
        # Try to extract title from the file
        title_match = re.search(r'Lesson \d+:\s*(.+?)(?:\n|$)', content)
        if title_match:
            title = title_match.group(1)
            audio_script = f"Episode {lesson_num}: {title}\n\n{audio_script}"
    
    return audio_script, theory_latex, problems_latex

def fix_latex_unicode(latex_content):
    """Fix common Unicode issues in LaTeX content."""
    replacements = {
        '✓': '\\checkmark',
        '×': '\\times',
        '∞': '\\infty',
        'α': '\\alpha',
        'β': '\\beta',
        'γ': '\\gamma',
        'δ': '\\delta',
        'ε': '\\varepsilon',
        'θ': '\\theta',
        'λ': '\\lambda',
        'μ': '\\mu',
        'π': '\\pi',
        'σ': '\\sigma',
        'τ': '\\tau',
        'φ': '\\phi',
        'ω': '\\omega',
        'Ω': '\\Omega',
        '∂': '\\partial',
        '∇': '\\nabla',
        '∈': '\\in',
        '∉': '\\notin',
        '⊂': '\\subset',
        '⊆': '\\subseteq',
        '∪': '\\cup',
        '∩': '\\cap',
        '≈': '\\approx',
        '≠': '\\neq',
        '≤': '\\leq',
        '≥': '\\geq',
        '→': '\\rightarrow',
        '⇒': '\\Rightarrow',
        '⇔': '\\Leftrightarrow',
        '∀': '\\forall',
        '∃': '\\exists',
        '∑': '\\sum',
        '∏': '\\prod',
        '∫': '\\int',
        '√': '\\sqrt',
        '±': '\\pm',
        '·': '\\cdot',
        '…': '\\ldots',
        '′': "'",
        '″': "''",
        '—': '---',
        '–': '--',
    }
    
    result = latex_content
    for unicode_char, latex_cmd in replacements.items():
        result = result.replace(unicode_char, latex_cmd)
    
    return result

def ensure_latex_packages(latex_content):
    """Ensure necessary LaTeX packages are included."""
    if '\\documentclass' not in latex_content:
        return latex_content
    
    required_packages = [
        '\\usepackage{amsmath, amssymb, amsthm}',
        '\\usepackage{geometry}',
        '\\usepackage{enumitem}',
        '\\usepackage{mdframed}',
        '\\usepackage{xcolor}',
        '\\usepackage{tikz}',
    ]
    
    # Check if packages are missing and add them
    for package in required_packages:
        package_name = package.split('{')[1].split(',')[0].split('}')[0]
        if package_name not in latex_content:
            # Insert after documentclass
            insert_pos = latex_content.find('\\begin{document}')
            if insert_pos > 0:
                latex_content = latex_content[:insert_pos] + package + '\n' + latex_content[insert_pos:]
    
    return latex_content

def process_lesson(lesson_num, source_dir, target_dir):
    """Process a single lesson."""
    source_file = source_dir / f"{lesson_num}.txt"
    if not source_file.exists():
        print(f"Warning: {source_file} not found")
        return False
    
    print(f"Processing Lesson {lesson_num}...")
    
    # Create lesson directory
    lesson_dir = target_dir / f"lesson_{lesson_num:02d}"
    lesson_dir.mkdir(exist_ok=True)
    
    # Extract components
    audio, theory, problems = extract_lesson_components(source_file)
    
    if not audio:
        print(f"  Warning: No audio script found for lesson {lesson_num}")
    if not theory:
        print(f"  Warning: No theory LaTeX found for lesson {lesson_num}")
    if not problems:
        print(f"  Warning: No problems LaTeX found for lesson {lesson_num}")
    
    # Save audio script
    if audio:
        audio_file = lesson_dir / "lesson_script.txt"
        with open(audio_file, 'w', encoding='utf-8') as f:
            f.write(audio)
        print(f"  Created: {audio_file}")
    
    # Process and save theory LaTeX
    if theory:
        theory = fix_latex_unicode(theory)
        theory = ensure_latex_packages(theory)
        theory_file = lesson_dir / f"lesson_{lesson_num:02d}.tex"
        with open(theory_file, 'w', encoding='utf-8') as f:
            f.write(theory)
        print(f"  Created: {theory_file}")
        
        # Compile to PDF
        try:
            result = subprocess.run(
                ['pdflatex', f'lesson_{lesson_num:02d}.tex'],
                cwd=lesson_dir,
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                print(f"  Compiled: lesson_{lesson_num:02d}.pdf")
            else:
                print(f"  Warning: Failed to compile theory PDF")
        except Exception as e:
            print(f"  Warning: Could not compile theory PDF: {e}")
    
    # Process and save problems LaTeX
    if problems:
        problems = fix_latex_unicode(problems)
        problems = ensure_latex_packages(problems)
        problems_file = lesson_dir / f"problems_{lesson_num:02d}.tex"
        with open(problems_file, 'w', encoding='utf-8') as f:
            f.write(problems)
        print(f"  Created: {problems_file}")
        
        # Compile to PDF
        try:
            result = subprocess.run(
                ['pdflatex', f'problems_{lesson_num:02d}.tex'],
                cwd=lesson_dir,
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                print(f"  Compiled: problems_{lesson_num:02d}.pdf")
            else:
                print(f"  Warning: Failed to compile problems PDF")
        except Exception as e:
            print(f"  Warning: Could not compile problems PDF: {e}")
    
    return True

def main():
    """Main processing function."""
    base_dir = Path("/home/archer/Desktop/ODE 50 Lessons Plan")
    source_dir = base_dir / "Lessons 19 and more"
    
    # Process lessons 19-50
    successful = 0
    failed = []
    
    for lesson_num in range(19, 51):
        try:
            if process_lesson(lesson_num, source_dir, base_dir):
                successful += 1
            else:
                failed.append(lesson_num)
        except Exception as e:
            print(f"Error processing lesson {lesson_num}: {e}")
            failed.append(lesson_num)
    
    print(f"\n{'='*50}")
    print(f"Processing complete!")
    print(f"Successfully processed: {successful} lessons")
    if failed:
        print(f"Failed lessons: {failed}")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()