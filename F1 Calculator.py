import json
import tkinter as tk
from tkinter import filedialog, messagebox
from difflib import SequenceMatcher

def calculate_f1_scores(annotator_file, ground_truth_file):
    with open(annotator_file, 'r') as file:
        annotator_data = [json.loads(line) for line in file]

    with open(ground_truth_file, 'r') as file:
        ground_truth_data = [json.loads(line) for line in file]

    tp_exact = 0
    fp_exact = 0
    fn_exact = 0
    tp_partial = 0
    fp_partial = 0
    fn_partial = 0

    for ground_truth_instance in ground_truth_data:
        ground_truth_annotations = ground_truth_instance.get('annotations', {}).get('named_entity', [])

        if not ground_truth_annotations:
            continue

        annotator_instance = max(annotator_data, key=lambda x: similarity_score(x, ground_truth_instance))
        annotator_annotations = annotator_instance.get('annotations', {}).get('named_entity', [])

        matched_annotations_exact = set()
        matched_annotations_partial = set()

        for ground_truth_entity in ground_truth_annotations:
            ground_truth_start = ground_truth_entity['start']
            ground_truth_end = ground_truth_entity['end']

            matched_annotator_entity_exact = None
            matched_annotator_entity_partial = None
            max_similarity_exact = 0
            max_similarity_partial = 0

            for annotator_entity in annotator_annotations:
                annotator_start = annotator_entity['start']
                annotator_end = annotator_entity['end']
                similarity = similarity_score(annotator_entity, ground_truth_entity)

                if (annotator_start, annotator_end) not in matched_annotations_exact and similarity > max_similarity_exact:
                    max_similarity_exact = similarity
                    matched_annotator_entity_exact = annotator_entity

                if similarity > max_similarity_partial:
                    max_similarity_partial = similarity
                    matched_annotator_entity_partial = annotator_entity

            if matched_annotator_entity_exact:
                tp_exact += 1
                matched_annotations_exact.add((matched_annotator_entity_exact['start'], matched_annotator_entity_exact['end']))
            else:
                fn_exact += 1

            if matched_annotator_entity_partial:
                tp_partial += 1
                matched_annotations_partial.add((matched_annotator_entity_partial['start'], matched_annotator_entity_partial['end']))
            else:
                fn_partial += 1

        fp_exact += len(annotator_annotations) - len(matched_annotations_exact)
        fp_partial += len(annotator_annotations) - len(matched_annotations_partial)

    precision_exact = tp_exact / (tp_exact + fp_exact) if tp_exact + fp_exact != 0 else 0
    recall_exact = tp_exact / (tp_exact + fn_exact) if tp_exact + fn_exact != 0 else 0
    f1_score_exact = 2 * (precision_exact * recall_exact) / (precision_exact + recall_exact) if precision_exact + recall_exact != 0 else 0

    precision_partial = tp_partial / (tp_partial + fp_partial) if tp_partial + fp_partial != 0 else 0
    recall_partial = tp_partial / (tp_partial + fn_partial) if tp_partial + fn_partial != 0 else 0
    f1_score_partial = 2 * (precision_partial * recall_partial) / (precision_partial + recall_partial) if precision_partial + recall_partial != 0 else 0

    return f1_score_exact, f1_score_partial


def similarity_score(entity1, entity2):
    text1 = entity1.get('text', '')
    text2 = entity2.get('text', '')
    return SequenceMatcher(None, text1, text2).ratio()


# Create the Tkinter root window
root = tk.Tk()
root.withdraw()  # Hide the root window

# Prompt the user to select the annotation file
messagebox.showinfo('Annotation File', 'Select the Annotation File')
annotator_file = filedialog.askopenfilename(title='Select Annotation File')

# Prompt the user to select the ground truth file
messagebox.showinfo('Ground Truth File', 'Select the Ground Truth File')
ground_truth_file = filedialog.askopenfilename(title='Select Ground Truth File')

if not annotator_file or not ground_truth_file:
    messagebox.showinfo('File Selection', 'File selection cancelled.')
else:
    f1_score_exact, f1_score_partial = calculate_f1_scores(annotator_file, ground_truth_file)
    messagebox.showinfo('F1 Scores', f'Exact Match F1 Score: {f1_score_exact:.2f}\nPartial Match F1 Score: {f1_score_partial:.2f}')
