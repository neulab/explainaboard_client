from __future__ import annotations

from enum import Enum
import json


# --- Copy-pasted from ExplainaBoard constants.py ---
class TaskType(str, Enum):
    text_classification = "text-classification"
    named_entity_recognition = "named-entity-recognition"
    qa_extractive = "qa-extractive"
    summarization = "summarization"
    machine_translation = "machine-translation"
    text_pair_classification = "text-pair-classification"
    aspect_based_sentiment_classification = "aspect-based-sentiment-classification"
    kg_link_tail_prediction = "kg-link-tail-prediction"
    qa_multiple_choice = "qa-multiple-choice"
    conditional_generation = "conditional-generation"
    word_segmentation = "word-segmentation"
    language_modeling = "language-modeling"
    chunking = "chunking"

    @staticmethod
    def list():
        return list(map(lambda c: c.value, TaskType))


class FileType(str, Enum):
    json = "json"
    tsv = "tsv"
    csv = "csv"
    conll = "conll"  # for tagging task such as named entity recognition
    datalab = "datalab"
    text = "text"

    @staticmethod
    def list():
        return list(map(lambda c: c.value, FileType))


# --- End copy-paste from ExplainaBoard ---


DEFAULT_METRICS: dict[TaskType, list[str]] = {
    TaskType.text_classification: ["Accuracy"],
    TaskType.named_entity_recognition: ["F1"],
    TaskType.qa_extractive: ["F1", "ExactMatch"],
    TaskType.summarization: ["rouge1", "rouge2", "rougeL", "length_ratio"],
    TaskType.machine_translation: ["bleu", "length_ratio"],
    TaskType.text_pair_classification: ["Accuracy"],
    TaskType.aspect_based_sentiment_classification: ["Accuracy"],
    TaskType.kg_link_tail_prediction: ["Hits", "MRR"],
    TaskType.qa_multiple_choice: ["Accuracy"],
    TaskType.conditional_generation: ["bleu", "length_ratio"],
    TaskType.word_segmentation: ["F1"],
    TaskType.language_modeling: ["LogProb"],
    TaskType.chunking: ["Accuracy"],
}


FILE_SUFFIX_MAP = {"txt": "text"}


def infer_file_type(file_path: str | None, task: TaskType):
    """
    Infer the type of the file from the file path and task type. Mostly looks at the
    suffix, tries to parse json and returns json if it works, then gives up otherwise.
    """
    if file_path is None:
        return None
    suffix = file_path.split(".")[-1]
    type_str = FILE_SUFFIX_MAP.get(suffix, suffix)
    if type_str in FileType.list():
        return type_str
    else:
        try:
            with open(file_path, "r") as fin:
                json.load(fin)
            return "json"
        except Exception:
            raise ValueError(
                f"Could not infer file type of {file_path}. Please "
                "specify the file type directly via the command line"
            )
