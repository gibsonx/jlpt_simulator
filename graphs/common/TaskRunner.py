from graphs.common.ExamGenerator import ExamGenerator
from langchain_core.prompts import ChatPromptTemplate
import importlib

def run(level: str, exam_type: str):
    """
    Generate exam outline for a given level and exam_type.
    Prompts are selected dynamically based on level.
    """
    try:
        # Dynamically import the module for the given level
        module_name = f"graphs.{level.lower()}.run"
        level_module = importlib.import_module(module_name)
    except ModuleNotFoundError:
        raise ValueError(f"No module found for level '{level}'. Expected module: {module_name}")

    # Build the prompt registry dynamically from the imported module
    PROMPT_REGISTRY: dict[str, ChatPromptTemplate] = {
        "full_exam": getattr(level_module, "full_exam_prompt", None),
        "fast_exam": getattr(level_module, "fast_exam_prompt", None),
        "reading": getattr(level_module, "reading_prompt", None),
        "listening": getattr(level_module, "listening_prompt", None),
        "grammar": getattr(level_module, "grammar_prompt", None),
        "vocab": getattr(level_module, "vocab_prompt", None),
    }

    # Case-insensitive exam_type lookup
    prompt = PROMPT_REGISTRY.get(exam_type.lower())
    if not prompt:
        raise ValueError(f"No prompt defined for exam_type: {exam_type}")

    # Generate and store exam
    exam_generator = ExamGenerator(level=level, exam_type=exam_type, db_collection=f"{level}_{exam_type}")
    inserted_id, outline = exam_generator._generate_and_store_paper(instruction=prompt)

    if inserted_id:
        print(f"✅ Exam outline stored successfully! Document ID: {inserted_id}")
    else:
        print("❌ Failed to generate or store exam outline. Check logs for details.")

    # Optionally inspect the outline object
    if outline:
        print("\nGenerated Outline:")
        print(outline)

if __name__ == "__main__":
    run(level="n2",exam_type="fast_exam")