from __future__ import division

import numpy as np
from plotly.offline import plot
import plotly.graph_objs as go


def create_csv_summary(labels, counts, summary_csv_path):

    # For calculating precision (remember the rows of a confusion matrix represent FN, columns represent FP)
    counts_transpose = np.matrix(counts).transpose().tolist()

    total_count = sum([sum(row_counts) for row_counts in counts])

    with open(summary_csv_path, "wb") as csv_file:
        csv_file.write("Total Count,{},\n\n".format(total_count))
        for idx, label in enumerate(labels):
            csv_file.write(label+",\n")
            num_TP = counts[idx][idx]               # i.e. the diagonals of confusion matrix are TP
            num_TP_FP = sum(counts_transpose[idx])  # i.e. summing the columns of confusion matrix
            num_TP_FN = sum(counts[idx])            # i.e. summing the rows of confusion matrix
            csv_file.write("Precision,{},\n".format(num_TP /num_TP_FP))
            csv_file.write("Recall,{},\n".format(num_TP / num_TP_FN))
            csv_file.write("\n")


def save_confusion_matrix(counts, x_and_y_labels, save_path, normalise_counts=False, main_title="Confusion Matrix"):

    if normalise_counts:
        # normalise rows (i.e. Actual class values) following http://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html#sphx-glr-auto-examples-model-selection-plot-confusion-matrix-py
        normalised_counts = []
        for one_class_counts in counts:
            normalised_counts.append([one_cell_count / sum(one_class_counts) for one_cell_count in one_class_counts])
        counts = normalised_counts

    # Plot
    colorscale = [[0, '#deebf7'], [1, '#3182bd']]  # custom colorscale
    # colorscale = [[0, '#ffeda0'], [1, '#f03b20']]  # custom colorscale


    trace = go.Heatmap(
        z=counts,
        x=x_and_y_labels,
        y=x_and_y_labels,
        colorscale=colorscale,
        showscale=True
    )

    # Add text labels to each grid cell
    annotations = []
    z = counts
    x = x_and_y_labels
    y = x_and_y_labels
    for n, row in enumerate(z):
        for m, val in enumerate(row):
            var = z[n][m]
            annotations.append(
                dict(
                    text=str(val),
                    x=x[m], y=y[n],
                    xref='x1', yref='y1',
                    font=dict(color='white' if val > 0.5 else 'black'),
                    showarrow=False)
            )

    # Create firgure from text labels and heatmap
    fig = go.Figure(data=[trace])
    fig['layout'].update(
        title=main_title,
        annotations=annotations,
        xaxis=dict(ticks='', side='bottom', title='Predicted'),
        # ticksuffix is a workaround to add a bit of padding
        yaxis=dict(ticks='', ticksuffix='  ', title='Actual', ),
        width=700,
        height=700,
        autosize=False
    )

    plot(fig, filename=save_path, show_link=False)


def main(prediction_actual_mappings, summary_csv_path=None, confusion_matrix_path=None, confusion_matrix_normalised_path=None):

    # Setting up plotly based on: https://plot.ly/python/heatmaps/
    x_and_y_labels = []
    counts = []
    if __name__ == '__main__':
        for predicted_class, actual_filenames in sorted(prediction_actual_mappings.items()):
            x_and_y_labels.append(predicted_class)

            row_counts = []
            for actual_class, filenames in sorted(actual_filenames.items()):
                # for filename in filenames:
                row_counts.append(len(filenames))
            counts.append(row_counts)

        # Transpose to follow standard of "Actual" on side axis, "Predicted" on top
        counts = np.matrix(counts).transpose().tolist()

    if summary_csv_path:
        create_csv_summary(x_and_y_labels, counts, summary_csv_path)

    if confusion_matrix_path:
        save_confusion_matrix(counts, x_and_y_labels, confusion_matrix_path, normalise_counts=False,
                              main_title="Confusion Matrix")

    if confusion_matrix_normalised_path:
        save_confusion_matrix(counts, x_and_y_labels, confusion_matrix_normalised_path, normalise_counts=True,
                              main_title="Confusion Matrix (Actual normalised)")

if __name__ == "__main__":
    prediction_actual_mappings = {
        "class1": {  # predicted label
            # actual label per image file:
            "class1": ["file1", "file2"],
            "class2": ["file3"],
            "class3": ["file4", "file5", "file6"],
        },
        "class2": {
            "class1": ["file7"],
            "class2": ["file8", "file9", "file10", "file11"],
            "class3": []
        },
        "class3": {
            "class1": [],
            "class2": ["file12", "file13", "file14"],
            "class3": ["file15", "file16", "file17"]
        }
    }

    main(prediction_actual_mappings, summary_csv_path="/tmp/summary.csv", confusion_matrix_path="/tmp/standard.html",
         confusion_matrix_normalised_path="/tmp/normalised.html")