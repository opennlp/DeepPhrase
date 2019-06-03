"""
Module containing common plotting utilities like plotting a scatter plot, line chart etc.
"""

import numpy as np
import matplotlib.pyplot as plt


"""
Given a list of data samples and a corresponding label list plots it and additionally saves it

Params:
--------
data_list - List of list containing the data points
color_list - List of colors which are used for filling the data points while plotting
group_list - List of class/group labels associated with a given data set
xlabel - String to label the X-axis with
ylabel - String to label the Y-axis with
title - String containing the title
save_filename - filename to which the plot is to be saved

Returns:
---------
None
"""


def save_and_plot_scatter(data_list,color_list,group_list,xlabel='X Values',ylabel='Y Values',title='Default Plot Title',save_filename='default.png'):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    for data, color, group in zip(data_list, color_list, group_list):
        x, y = data[:,0], data[:,1]
        ax.scatter(x, y, alpha=0.8, c=color, edgecolors='none', s=3, label=group)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
    plt.title(title)
    plt.legend(loc='best')
    plt.savefig(save_filename)
    plt.show()


"""
Given a data set plots a histogram and saves it

Params:
--------
data - the dataset whose histogram is to be plotted
bins - the bins to divide the data into (default value set to 20)
xlabel - String to label the X-axis with
ylabel - String to label the Y-axis with
title - String containing the title
save_filename - filename to which the plot is to be saved

Returns:
--------
None
"""


def save_and_plot_histogram(data,bins=20,xlabel='X Values',ylabel='Y Values',title='Default Plot Title',save_filename='default.png'):
    plt.hist(data,bins=bins)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.savefig(save_filename)
    plt.show()


"""
Class which contains utility methods for plotting clusters

Params:
X - x coordinate values of the data
Y - y coordinate values of the data
cluster_label_list - list containing the labels for each data point
size - size of the markers of data (default value 7)

Returns:
None
"""


class VisualizeClusters:
    def __init__(self, X, Y, cluster_label_list, size=7):
        self.X = X
        self.Y = Y
        self.colors = cluster_label_list
        self.marker_size = size

    def plot_scatter_chart(self, x_label, y_label, title, filename_to_save, show_plot=True):
        plt.scatter(self.X, self.Y, c=self.colors, s=self.marker_size)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.legend()
        plt.legend(loc='best')
        plt.title(title)
        plt.savefig(filename_to_save)
        if show_plot:
            plt.show()


"""
Utility function to visualize the decision boundaries of the classifiers

Params:
-------
data - Training data for which the classifiers have to be trained
class_labels - The class label list for each point of the training data
classifier_list - List of classifier objects whose decision boundaries have to be plotted
classifier_name_list - Names of the classifiers used
step_size - size of the steps used to generate the meshgrid (default value 0.2)
xlabel - Label for x-axis set to default value
ylabel - Label for y-axis set to default value

Returns:
--------
"""


def visualize_classifier_decision_boundaries(data,class_labels,classifier_list,classifier_name_list,step_size=0.2,xlabel='Default X',ylabel='Default Y'):
    train_data, train_labels = data, class_labels
    x_min, x_max = train_data[:, 0].min() - 1, train_data[:, 0].max() + 1
    y_min, y_max = train_data[:, 1].min() - 1, train_data[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, step_size), np.arange(y_min, y_max, step_size))

    for index, classifier in enumerate(classifier_list):
        classifier.fit(train_data, train_labels)
        Z = classifier.predict(zip(xx.ravel(), yy.ravel()))
        Z = Z.reshape(xx.shape)
        plt.subplot(2, 3, index + 1)
        plt.subplots_adjust(wspace=0.5, hspace=0.5)
        plt.contourf(xx, yy, Z, cmap=plt.cm.Spectral, alpha=0.6)
        plt.scatter(train_data[:, 0], train_data[:, 1], c=train_labels, cmap=plt.cm.gist_rainbow, alpha=0.3)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.xlim(xx.min(), xx.max())
        plt.ylim(yy.min(), yy.max())
        plt.xticks(())
        plt.yticks(())
        plt.title(classifier_name_list[index])
        print(index)

    plt.show()


"""
Given a set of data points and data labels draws a line plot

Params:
--------
data_list - List of list containing the data points
data_label - String labels for each data point
xlabel - Label for x-axis set to default value
ylabel - Label for y-axis set to default value

Returns:
--------
None
"""


def generate_and_save_lineplot(data_list,data_label,xlabel='Default X Label',ylabel='Default Y label'):
    if len(data_list) != len(data_label):
        raise RuntimeError("The data labels and data points must be of same length")
    fig, ax = plt.subplots()
    for data,label in zip(data_list,data_label):
        ax.plot(data, label=label)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
    ax.legend(loc='best',shadow=True)
    plt.ylim((0,100))
    plt.show()

