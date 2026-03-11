import os
import re

PROJECT_ROOT = "agentic_rag"

# patterns to fix
replacements = {
    r"from agentic_rag.query_layer": "from agentic_rag.query_layer",
    r"from agentic_rag.retrieval_layer": "from agentic_rag.retrieval_layer",
    r"from agentic_rag.reasoning_layer": "from agentic_rag.reasoning_layer",
    r"from agentic_rag.memory": "from agentic_rag.memory",
    r"from agentic_rag.llm": "from agentic_rag.llm",
}

for root, dirs, files in os.walk(PROJECT_ROOT):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)

            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            new_content = content

            for old, new in replacements.items():
                new_content = re.sub(old, new, new_content)

            if new_content != content:
                print(f"Fixing imports in: {path}")
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new_content)

print("Import fix completed.")