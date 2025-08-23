# Lessons Extraction Summary

## Extracted Lessons (09-18)

All lessons have been successfully extracted from `/home/archer/Desktop/ODE 50 Lessons Plan/prompts/lessons.txt` and saved in their respective directories as raw text files.

### Lesson Details:

| Lesson | Title | Lines in Original | Lines Extracted | Location |
|--------|-------|------------------|-----------------|----------|
| 09 | Direction Fields and Isoclines - Visualizing Solutions | 1-258 | 258 | `lesson_09/lesson_09_raw.txt` |
| 10 | Qualitative Behavior Without Solving | 258-627 | 370 | `lesson_10/lesson_10_raw.txt` |
| 11 | Direct Integration - The Simplest ODEs | 628-1164 | 537 | `lesson_11/lesson_11_raw.txt` |
| 12 | Separable Equations - Complete Method and Tricks | 1165-1787 | 623 | `lesson_12/lesson_12_raw.txt` |
| 13 | Implicit Solutions and Singular Solutions | 1788-2484 | 697 | `lesson_13/lesson_13_raw.txt` |
| 14 | Linear First-Order ODEs - The Standard Method | 2485-2990 | 506 | `lesson_14/lesson_14_raw.txt` |
| 15 | Integrating Factor Technique - Deep Dive | 2991-3627 | 637 | `lesson_15/lesson_15_raw.txt` |
| 16 | Variation of Constants for First-Order ODEs | 3628-4171 | 544 | `lesson_16/lesson_16_raw.txt` |
| 17 | Homogeneous Equations - The y/x Substitution | 4172-4637 | 466 | `lesson_17/lesson_17_raw.txt` |
| 18 | Bernoulli Equations - The Power Transform | 4638-5203 | 566 | `lesson_18/lesson_18_raw.txt` |

## Content Structure

Each raw lesson file contains:
1. **Audio Lesson Script** - Conversational style teaching content
2. **LaTeX Theory Document** - Formal mathematical content with theorems, definitions, and examples
3. **Practice Problems Set** - Exercises with varying difficulty levels
4. **Additional materials** - Answer keys, hints, and exam tips

## Next Steps

These raw text files are ready to be processed into the structured format used for lessons 07 and 08:
- Split into separate files: `lesson_script.txt`, `lesson_XX.tex`, `problems_XX.tex`
- Compile LaTeX files to PDFs
- Organize and clean up formatting as needed

## Directory Structure

```
ODE 50 Lessons Plan/
├── lesson_07/          (completed with PDFs)
├── lesson_08/          (completed with PDFs)
├── lesson_09/          (raw text extracted)
├── lesson_10/          (raw text extracted)
├── lesson_11/          (raw text extracted)
├── lesson_12/          (raw text extracted)
├── lesson_13/          (raw text extracted)
├── lesson_14/          (raw text extracted)
├── lesson_15/          (raw text extracted)
├── lesson_16/          (raw text extracted)
├── lesson_17/          (raw text extracted)
├── lesson_18/          (raw text extracted)
└── prompts/
    └── lessons.txt     (source file)
```