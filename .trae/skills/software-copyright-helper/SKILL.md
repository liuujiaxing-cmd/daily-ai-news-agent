---
name: "software-copyright-helper"
description: "Generates required documentation for Software Copyright Registration (软著), including cleaned source code and user manual. Invoke when user mentions 'copyright', '软著', or asks to generate copyright files."
---

# Software Copyright Helper

This skill helps users generate the two mandatory documents for Software Copyright Registration (计算机软件著作权) in China.

## Capabilities

1.  **Generate Source Code Document (SourceCode_Copyright.txt)**
    -   Scans the codebase for source files (e.g., .swift, .java, .py, .js, .cpp).
    -   Removes all comments (single-line `//` and block `/* */`).
    -   Removes empty lines.
    -   Consolidates content into a single text file.
    -   Ensures the output is clean and ready for Word document formatting (usually requiring first 30 and last 30 pages).

2.  **Generate User Manual Draft (UserManual.md)**
    -   Creates a structured user manual template.
    -   Includes standard sections: Software Overview, Installation, Features, Settings, and FAQ.

## Instructions for Agent

When this skill is invoked:

1.  **Identify the Project Root**: Confirm the path of the codebase to be processed.
2.  **Identify File Types**: Ask or infer the main programming language (e.g., `.swift` for iOS, `.java` for Android).
3.  **Execute Code Extraction**:
    -   Use `find` and `sed` commands to clean and extract code.
    -   Example command for Swift:
        ```bash
        find . -name "*.swift" -print0 | xargs -0 cat | sed '/^[[:space:]]*\/\//d' | sed '/^[[:space:]]*$/d' > SourceCode_Copyright.txt
        ```
    -   *Note*: Adjust the command for different languages (e.g., `#` for Python).
4.  **Create User Manual**:
    -   Generate a `UserManual.md` file with project-specific context (if known).
5.  **Report**: Inform the user where the files are saved and next steps (e.g., "Convert to Word/PDF").

## Example Output

-   `SourceCode_Copyright.txt`: Contains 3000+ lines of pure code.
-   `UserManual.md`: A 5-section user guide ready for export.
