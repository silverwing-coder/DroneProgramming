from sklearn.model_selection import train_test_split
from sklearn import (datasets, model_selection as skms, metrics, dummy, neighbors, naive_bayes)
import pandas as pd
import pickle

data = pd.read_csv("dt_a0.csv")
id_ftr = data.drop(['Index'],axis=1).values
id_tgt = data['Index'].values

# tts = skms.train_test_split(id_ftr, id_tgt, test_size=0.25, random_state=0)
tts = skms.train_test_split(id_ftr, id_tgt, test_size=0.3)
(train_ftr, test_ftr, train_tgt, test_tgt) = tts
# print(train_ftr)

# model = neighbors.KNeighborsClassifier(n_neighbors=3)
model = naive_bayes.CategoricalNB()
# model = naive_bayes.GaussianNB()
model.fit(train_ftr, train_tgt)

pred = model.predict(test_ftr)
print("Accuracy: ", metrics.accuracy_score(test_tgt, pred))
print(metrics.classification_report(test_tgt, pred))
cm = metrics.confusion_matrix(test_tgt, pred)
print("Confusion Matrix: ", cm, sep="\n")

#
# fpickle = open('kncpickle_file', 'wb')
# pickle.dump(model, fpickle)
# fpickle.close()

# ld_model = pickle.load(open('kncpickle_file', 'rb'))
# result = ld_model.predict(test_ftr)
#
# print("Load-Accuracy: ", metrics.accuracy_score(test_tgt, result))
#
# cm = metrics.confusion_matrix(test_tgt, result)
# print("Load-Confusion Matrix: ", cm, sep="\n")
