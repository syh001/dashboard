<mark><strong><font face="courier New" color=#1E90FF>数据预处理步骤</font><strong></mark>  



**扫描数据**  
1、按列读取，打印每列数据的数据类型  
data_scan_type()  
2、如果存在错误更改类型  
data_change_type(column)  


**将数据按照一定规则分组**  
1、按日期分组  
check_data_by_date(date)  
2、按某一条件分组  
check_data_with_criteria(criteria, threshold)

**缺失值发现**  
1、显示缺失%数据的行  
detect_nan_by_row(threshold)  
2、显示缺失%数据的列  
detect_nan_by_column(threshold)  

**缺失值处理**  
1、用均值、中位数、众数填充(默认按列)  
fill_nan_data(criteria)  
2、删除(按行或列)  
delete_nan_data（row/column）  

**异常值发现**  
1、3sigma原则找出  
abnormal_check_3sigma()  

**重复行的处理**  
1、保留  
process_multi_rows(threshold)  

**数据的标准化和归一化**  
process_data_standardization()  
process_data_normalization()  

**数据导出**  
export_data(format)  

#!可能存在 需要查看数据分布决定是否删除、或删除一部分的 情况（引入可视化中的函数模块）



