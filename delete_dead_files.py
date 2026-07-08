import os
import sys

def remove_file(filepath):
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"Deleted: {filepath}")
        else:
            print(f"Not found: {filepath}")
    except Exception as e:
        print(f"Error deleting {filepath}: {e}")

remove_file(r"d:\Traveler LLM\src\domain\entities\dataset.py")
remove_file(r"d:\Traveler LLM\src\domain\entities\model_version.py")

# Verify import
try:
    from src.pipelines.learning_pipeline import LearningPipeline
    print("Verification Passed: LearningPipeline loaded successfully.")
except Exception as e:
    print(f"Verification Failed: {e}")
    sys.exit(1)
