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
    qa_open_domain = "qa-open-domain"
    qa_tat = "qa-tat"
    conditional_generation = "conditional-generation"
    word_segmentation = "word-segmentation"
    language_modeling = "language-modeling"
    chunking = "chunking"
    cloze_mutiple_choice = "cloze-multiple-choice"
    cloze_generative = "cloze-generative"
    grammatical_error_correction = "grammatical-error-correction"
    nlg_meta_evaluation = "nlg-meta-evaluation"
    tabular_regression = "tabular-regression"
    tabular_classification = "tabular-classification"
    argument_pair_extraction = "argument-pair-extraction"

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
    TaskType.kg_link_tail_prediction: [
        "Hits1",
        "Hits2",
        "Hits3",
        "Hits5",
        "Hits10",
        "MRR",
    ],
    TaskType.qa_multiple_choice: ["Accuracy"],
    TaskType.qa_open_domain: ["ExactMatch", "F1"],
    TaskType.qa_tat: ["QATatExactMatch", "QATatF1"],
    TaskType.conditional_generation: ["bleu", "length_ratio"],
    TaskType.word_segmentation: ["F1"],
    TaskType.language_modeling: ["LogProb"],
    TaskType.chunking: ["Accuracy"],
    TaskType.cloze_mutiple_choice: ["Accuracy", "CorrectCpount"],
    TaskType.cloze_generative: ["CorrectCount"],
    TaskType.grammatical_error_correction: ["SeqCorrectCount"],
    TaskType.nlg_meta_evaluation: ["SegKtauCorr", "SysPearsonCorr"],
    TaskType.tabular_regression: ["RMSE", "AbsoluteError"],
    TaskType.tabular_classification: ["Accuracy"],
    TaskType.argument_pair_extraction: ["F1"],
}

FILE_SUFFIX_MAP = {"txt": "text"}

CUSTOM_DATASET_REQUIRED_COLUMNS: dict[TaskType, list[str]] = {
    TaskType.text_classification: ["text", "true_label"],
    TaskType.qa_extractive: ["context", "question", "answers"],
    TaskType.summarization: ["source", "reference"],
    TaskType.machine_translation: ["source", "reference"],
    TaskType.text_pair_classification: ["text1", "text2", "true_label"],
    TaskType.aspect_based_sentiment_classification: ["aspect", "text", "true_label"],
    TaskType.kg_link_tail_prediction: [
        "true_head",
        "true_head_decipher",
        "true_link",
        "true_tail",
        "true_tail_decipher",
    ],
    TaskType.qa_multiple_choice: ["context", "options", "question", "answers"],
    TaskType.qa_open_domain: ["question", "answers"],
    TaskType.conditional_generation: ["source", "reference"],
    TaskType.language_modeling: ["text"],
    TaskType.cloze_mutiple_choice: ["context", "options", "question_mark", "answers"],
    TaskType.cloze_generative: ["context", "hint", "question_mark", "answers"],
    TaskType.grammatical_error_correction: ["text", "edits"],
    TaskType.tabular_regression: ["true_value"],
    TaskType.tabular_classification: ["true_label"],
}

SYSTEM_OUTPUT_REQUIRED_COLUMNS: dict[TaskType, list[str]] = {
    TaskType.text_classification: ["predicted_label"],
    TaskType.qa_extractive: ["predicted_answers"],
    TaskType.summarization: ["hypothesis"],
    TaskType.machine_translation: ["hypothesis"],
    TaskType.text_pair_classification: ["predicted_label"],
    TaskType.aspect_based_sentiment_classification: ["predicted_label"],
    TaskType.kg_link_tail_prediction: ["predict", "predictions", "true_rank"],
    TaskType.qa_multiple_choice: ["predicted_answers"],
    TaskType.qa_open_domain: ["predicted_answer"],
    TaskType.qa_tat: ["predicted_answer", "predicted_answer_scale"],
    TaskType.conditional_generation: ["hypothesis"],
    TaskType.language_modeling: ["log_probs"],
    TaskType.cloze_mutiple_choice: ["predicted_answers"],
    TaskType.cloze_generative: ["predicted_answers"],
    TaskType.grammatical_error_correction: ["predicted_edits"],
    TaskType.nlg_meta_evaluation: ["auto_scores"],
    TaskType.tabular_regression: ["predicted_value"],
    TaskType.tabular_classification: ["predicted_label"],
    TaskType.argument_pair_extraction: ["pred_tags"],
}


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
