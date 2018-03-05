2018.3.5

pandas作为数据处理工具很好，但总是学了忘，忘了学，今天自己写一小段“备忘录”。
以下捞干的说

1. pandas里的两种基础数据表
    有两种：series和dataframe，我个人认为如果是一维数据就用series，二维数据就用dataframe，这个认识应该比较片面。

2. series的使用

3. dataframe的使用
    3.1. 生成(Creating the dataframe)
        按列填写数据（字典中一个key下的value是一列），字典的key为列标签
        df = pd.DataFrame(一个存放数据的字典，index=[指定用于检索的列号，例如1，2]) 
        按行填写数据（二维list中的每个一维list是一行，没有列名，列名由后续columns给出）
        df = pd.DataFrame(二维list，index=[指定用于检索的列号，例如1，2]，columns= [列标签，可用1，2，3这样的数字或字符串 ])
        如果检索是多层级的，可以如下定义
        df = pd.DataFrame( {“a”:[4,5,6],"b":[7,8,9],"c":[10,11,12]} ,index = pd.MultiIndex.from_tuples([('d',1),('d',2),('e',2)],names=['n','v'])))
        
    3.2 tidy data整洁的数据
        Wickham的Tidy data包含以下共性：每个变量构成一列；每次观测构成一行；每种观测单元构成一个表格。
        Tidy data补充了pandas的向量化操作。pandas将在你操作数据时自动的保持意见（我猜是保证数据为tidy）。No other format works as intuitively with pandas.
    
    3.3 Reshaping Data重塑数据表格式（change the layout of a data set）
        1.如果需要将原表的第一列作为第一层级，从di
    
