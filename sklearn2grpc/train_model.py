from sklearn import datasets
from sklearn.pipeline import Pipeline
import joblib
from sklearn.ensemble import RandomForestClassifier

if __name__ == "__main__":
    iris = datasets.load_iris()
    X, y = iris.data, iris.target
    clf = RandomForestClassifier()
    p = Pipeline([('clf', clf)])
    p.fit(X, y)

    filename_p = './IrisClassifier.pkl'
    joblib.dump(p, filename_p)
    print('Model saved!')