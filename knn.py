
def get_data():
    f = open("data.csv")
    X = []
    Y = []
    for line in f.read().split("\n"):
        if line == "": continue
        data = line.split(", ")
        Y.append(data[0])
        X.append([int(i)/256 for i in data[1:]])
    f.close()
    return X, Y

def seperate_data(X, Y, ratio):
    index = int(len(X)*ratio)
    return X[:index], Y[:index], X[index:], Y[index:]

def get_distance(x1, x2):
    total = 0
    for i in range(len(x1)):
        total += (x1[i]-x2[i])**2
    return (total)**0.5

def KNN(X, Y, data, k=3):
    nearest_values = []
    nearest_labels = []
    for _ in range(k):
        nearest_values.append(9999)
        nearest_labels.append(9999)
    for i in range(len(X)):
        dist = get_distance(X[i], data)
        for j in range(k):
            if dist < nearest_values[j]:
                nearest_values[j] = dist
                nearest_labels[j] = Y[i]
                break
    table = {}
    for label in nearest_labels:
        if label not in table:
            table[label] = 0
        else:
            table[label] += 1
    best_value = -1
    best_label = None
    for label, value in table.items():
        if value > best_value:
            best_value = value
            best_label = label
    return best_label

def main():
    X, Y = get_data()
    X_train, Y_train, X_test, Y_test = seperate_data(X, Y, 0.8)

    correct = 0
    for index in range(len(X_test)):
        label = KNN(X_train, Y_train, X_test[index], k=5)
        if label == Y_test[index]:
            correct += 1
    print("accuracy: ", correct/len(X_test))
    
    # while True:
    #     index = int(input("index: "))
    #     label = KNN(X_train, Y_train, X_test[index], k=3)
    #     print("found label:", label)
    #     print("real label :", Y_test[index])

if __name__ == "__main__":
    main()
