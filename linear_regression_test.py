import sklearn
from sklearn import linear_model
import pandas
import numpy

#csv disponível em:
#https://archive.ics.uci.edu/ml/datasets/Student+Performance
data = pandas.read_csv("student-mat.csv", sep=";")
#colunas selecionadas para serem analisadas
data = data[["studytime", "failures", "freetime", "health", "absences", "G1", "G2", "G3"]]
print(data.head(), "\n")

#será treinado para  prever a coluna G3
predict = "G3"

#armazena todos os dados da coluna G3 em Y, o resto fica em x
x = numpy.array(data.drop([predict], 1))
y = numpy.array(data[predict])

#x_train e y_train são dados do X e Y que serão usados para treinar
#x_test e y_test são dados do X e Y que serão usados para testar depois que estiver treinado
#test_size é a porcentagem do X e Y que é usado para testar
x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=0.2)
linear = linear_model.LinearRegression()
#cria uma linha de intercepção baseado nos dados usados para treinar
linear.fit(x_train, y_train)
#porcentagem de acertos que garante
score = linear.score(x_test, y_test)
print("Acertos: ", round(score * 100, 2), "%")
#os valores dos coeficientes e da intercepção
print("Coeficientes: ", linear.coef_)
print("Intercepção: ", linear.intercept_, "\n")

#demonstração:
#faz previsões de acordo com os valores do x_test
predictions = linear.predict(x_test)
for index in range(len(predictions)):
    #printa o valor da previsão, os valores usados na previsão e o resultado que deveria ter
    print((round(predictions[index], 1)), x_test[index], y_test[index])
