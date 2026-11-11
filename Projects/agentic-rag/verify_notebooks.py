"""Run each notebook in a separate kernel; do not modify the submitted files."""
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import sys

import nbformat
from jupyter_client.kernelspec import KernelSpecManager
from nbclient import NotebookClient

names = ("LangGraph_Agentic RAG 篇.ipynb", "LangGraph-CRAG 篇.ipynb", "LangGraph_-Adaptive-RAG 篇.ipynb")
root = Path(__file__).resolve().parent
with TemporaryDirectory() as scratch:
    # Ensure the kernel uses this environment's interpreter instead of a global python3.
    spec = Path(scratch) / "kernels" / "course-rag"
    spec.mkdir(parents=True)
    (spec / "kernel.json").write_text(json.dumps({
        "display_name":"課堂 RAG", "language":"python",
        "argv":[sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"],
    }))
    from jupyter_client import AsyncKernelManager
    for name in names:
        notebook = nbformat.read(root / name, as_version=4)
        nbformat.validate(notebook)
        km = AsyncKernelManager(kernel_name="course-rag",
             kernel_spec_manager=KernelSpecManager(kernel_dirs=[str(spec.parent)]))
        client = NotebookClient(notebook, km=km, timeout=90, allow_errors=False,
                                resources={"metadata":{"path":scratch}})
        try:
            client.execute()
            print("PASS", name)
            for c in notebook.cells:
                for o in c.get("outputs", []):
                    if o.output_type == "stream" and o.name == "stdout":
                        print(o.text.strip())
        finally:
            if km.has_kernel:
                import asyncio
                asyncio.run(km.shutdown_kernel(now=True))
