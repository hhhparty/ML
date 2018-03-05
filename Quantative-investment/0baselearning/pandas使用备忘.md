2018.3.5

pandas作为数据处理工具很好，但总是学了忘，忘了学，今天自己写一小段“备忘录”。 以下捞干的说

## 1. pandas里的两种基础数据表
有两种：series和dataframe，我个人认为如果是一维数据就用series，二维数据就用dataframe，这个认识应该比较片面。

## 2. series的使用
暂时略过
## 3. dataframe的使用 
### 3.1. 生成(Creating the dataframe)        
1. 按列填写数据（字典中一个key下的value是一列），字典的key为列标签.
df = pd.DataFrame(一个存放数据的字典，index=[指定用于检索的列号，例如1，2])

2. 按行填写数据（二维list中的每个一维list是一行，没有列名，列名由后续columns给出）        
df = pd.DataFrame(二维list，index=[指定用于检索的列号，例如1，2]，columns= [列标签，可用1，2，3这样的数字或字符串 ])        

3. 如果检索是多层级的，可以如下定义        
df = pd.DataFrame( {“a”:[4,5,6],"b":[7,8,9],"c":[10,11,12]} ,index = pd.MultiIndex.from_tuples([('d',1),('d',2),('e',2)],names=['n','v'])))

### 3.2 tidy data整洁的数据        
Wickham的Tidy data包含以下共性：每个变量构成一列；每次观测构成一行；每种观测单元构成一个表格。        
Tidy data补充了pandas的向量化操作。pandas将在你操作数据时自动的保持意见（我猜是保证数据为tidy）。
No other format works as intuitively with pandas.

### 3.3 Reshaping Data重塑数据表格式（change the layout of a data set）        
1. Gather columns into rows (把列按行层级排列，不是矩阵转置)
pd.melt(df)
2. Spread rows into columns(melt的逆操作)
df.pivot(columns='var',values='val')
3. Append rows of DataFrames(合并两个列相同的表)
pd.concat([df1,df2])
4. Append columns of DataFrames(合并两个行相同的表,axis=1指定按哪一列对齐)
pd.concat([df1,df2],axis=1)

### 3.4 Subset observation（Rows）行子集试图（按行取子集）
1. Extract rows that meet logical criteria 抽取满足逻辑条件的行
df[df.length > 7]
2. Remove duplicate rows (only considers columns)
df.drop_duplicates()
3. Select first n rows(从1计数)
df.head(n)
4. Select last n rows(从1计数）
df.tail(n)
5. Randomly select fraction of rows(随机采样50%的行)
df.sample(frac=0.5）
6. Randomly select n rows(随机采样n=3行）
df.sample(n=3)
7. Select rows by position(按位置选行，位置从0计数）
df.iloc[10:20]
8. Select and order top n entires
df.nlargest(n,'value')选取'value'这一列中值最大的n行，并排序
9. Select and order bottom n entries
df.nsmallest(n,'value')选取‘value’列中值最小的n行，并排序

### 3.5 Subset Variables 按列选取子集
1. Select multiple columns with specific names.
df[['width','length','species']]
2. Select single column with specific name.
df['width'] or df.width
3. Select columns whose name matches regular expression regex
df.filter(regex = 'regex')
regex examples: '\.' 表示要匹配包含一个点'.'的字符串； 'Length$'表示要匹配以Length为结尾的字串； '^Sepal' 表示要匹配一个以单词Sepal开始的字串； '^x[1-5]$' 表示要匹配一个以x为开始，以数字1，2，3，4，5其中之一为结束的字串； ''^(?!Species$).*' 表示要匹配一个不包含Species的字串。
4. Select all columns bettween x2 and x4 (inclusive) x4也包含在内
df.loc[:,'x2':'x4'] 注意loc是按标签选，iloc是按位置选
5. Select columns in positions 1,2 and 5 (first columns is 0)
df.iloc[:,[1,2,5]]
6. Select rows meeting logical condition, and only the specific columns.
df.loc[df['a'] > 10, ['a','b','c' ]]

### 3.6 pandas中的几个判断逻辑
1. 判断Group membership
df.column.isin(values)
2. 判断空值 is NaN
pd.isnull(obj)
3. is not NaN
pd.notnull(obj)
4. logical and , or , not ,xor ,any ,all
&,|,~,^,df.any(),df.all()
5. less than, greater than, equals, not equal to, less than or equals, greater than or equals
<, >, ==, !=, <=, >= 



    
