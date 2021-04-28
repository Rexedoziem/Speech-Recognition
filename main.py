import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

# Define sample labels
true_labels = [2, 0, 0, 2, 4, 4, 1, 0, 3, 3, 3]
pred_labels = [2, 1, 0, 2, 4, 3, 1, 0, 1, 3, 3]

#Create confusion matrix
confusion_matrix = confusion_matrix(true_labels, pred_labels)

# Visualize confusion matrix
plt.imshow(confusion_matrix, interpolation='nearest', cmap=plt.cm.gray)
plt.title('confusion matrix')
plt.colorbar()
ticks = np.arange(5)
plt.xticks(ticks, ticks)
plt.yticks(ticks, ticks)
plt.ylabel('True labels')
plt.xlabel('Predicted labels')
plt.show()

# Classification report
targets = ['class-0', 'class-1', 'class-2', 'class-3', 'class-4']
print('/n', classification_report(true_labels, pred_labels, target_names=targets))
