import numpy as np 
# from sklearn import sklearn
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

data = np.loadtxt("../Bank_Customer.csv",skiprows=1,dtype=str,delimiter=',')

'''
Your work
非數值型資料需轉換成數值型資料 (country, gender)
去除掉無意義的特徵類別 (customer_id)
標準化特徵 (StandardScaler)
'''
# 將 country 由文字轉換成數值
# France = 0、Germany = 1、Spain = 2
data[:, 2] = np.where(
    data[:, 2] == "France",
    0,
    np.where(data[:, 2] == "Germany", 1, 2),
)

# 將 gender 由文字轉換成數值
# Female = 0、Male = 1
data[:, 3] = np.where(
    data[:, 3] == "Female",
    0,
    1,
)

# 刪除無助於預測的 customer_id 欄位
data = np.delete(data, 0, axis=1)

# 將處理完成的資料從文字型態轉換成數值型態
data = data.astype(float)

# 最後一欄 churn 是預測答案，其餘欄位是輸入特徵
x = data[:, :-1]
y = data[:, -1]

# 將輸入特徵標準化
scaler = StandardScaler()
x = scaler.fit_transform(x)

# 合併標準化後的特徵與 churn
pre_data = np.column_stack((x, y))



np.savetxt("Bank_Customer_Preprocessed.csv", pre_data, delimiter=",")


from sklearn.linear_model import LogisticRegression 
# 決策分類器
clf = LogisticRegression()

'''
Your work
切割 data 為 x_train, x_test, y_train, y_test
請學習 train_test_split 的使用方法
'''
# 將資料切割為 70% 訓練資料、30% 測試資料
x_train, x_test, y_train, y_test = train_test_split(
    pre_data[:, :-1],
    pre_data[:, -1],
    test_size=0.3,
    random_state=42
)

# 顯示訓練資料與測試資料的數量
print("Training data:", x_train.shape)
print("Testing data:", x_test.shape)

# 使用訓練集來訓練我們的分類器
clf.fit(x_train, y_train)
# 測試資料集中進行預測
pred = clf.predict(x_test)

#print (pred) # 預測分類，即客戶是否流失
#print (y_test) # 分類
print (str(accuracy_score(pred, y_test)*100 ) + "% ")   # 預測精度 