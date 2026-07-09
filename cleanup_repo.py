import shutil
from pathlib import Path


def run_cleanup():
    root = Path.cwd()

    # 1. Delete legacy UI pages
    pages_dir = root / "src" / "ui" / "pages"
    if pages_dir.exists():
        print(f"✅ Deleting legacy directory: {pages_dir}")
        shutil.rmtree(pages_dir)

    # 2. Delete legacy prompt file
    old_prompt = root / "prompts" / "travel_v1.md"
    if old_prompt.exists():
        print(f"✅ Deleting legacy prompt: {old_prompt}")
        old_prompt.unlink()

    # 3. Clean all __pycache__
    print("✅ Sweeping __pycache__ directories...")
    for p in root.rglob("__pycache__"):
        if p.is_dir():
            shutil.rmtree(p)

    # 4. Resolve GitHub Workflows
    pipeline1 = root / ".github" / "workflows" / "pipeline.yml"
    pipeline2 = root / ".github" / "workflows" / "ml-pipeline.yml"

    if pipeline1.exists() and pipeline2.exists():
        print(f"✅ Removing duplicate workflow: {pipeline1}")
        pipeline1.unlink()

    # 5. Fix Requirements Hygiene
    req_file = root / "requirements.txt"
    req_dev_file = root / "requirements-dev.txt"

    if req_file.exists():
        content = req_file.read_text(encoding="utf-8")
        if "# ==================== Development ====================" in content:
            print("✅ Splitting requirements.txt into production and development files...")
            parts = content.split("# ==================== Development ====================")
            prod_reqs = parts[0].strip()

            # Create req-dev.txt
            dev_reqs = "pytest==8.0.0\npytest-cov==4.1.0\nblack==24.0.0\nruff==0.3.0\npre-commit==3.6.0\n"
            req_dev_file.write_text(dev_reqs, encoding="utf-8")

            # Update req.txt
            req_file.write_text(prod_reqs + "\n", encoding="utf-8")

    print("\n🚀 Phase 1 and Phase 3 Cleanup Complete!")


if __name__ == "__main__":
    run_cleanup()
