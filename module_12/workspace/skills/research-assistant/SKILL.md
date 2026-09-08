---
name: research-assistant
description: Orchestrates an end-to-end research task by creating a structured todo plan, examining filesystem assets, and synthesizing a comprehensive final report.
---
# Research Assistant Skill
1. **Initialize Task Planning**: Call `write_todos` to track current task lists.
2. **Examine Sources**: Discover files through `ls` and parse content safely using `read_file`.
3. **Synthesize**: Format clean outputs using structured Markdown components.
