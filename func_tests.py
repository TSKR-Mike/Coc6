"""
data = [1, 2, 3, 4, 5, 10, 4, 5, 10, 4, 5]

    计算平均值、最大值、最小值中位数、众数、方差、标准差等

from scipy import stats
import numpy as np
mean = np.mean(data)#平均值
max_value = np.max(data)#最大值
min_value = np.min(data)#最小值
median = np.median(data)#中位数
mode = stats.mode(data)#众数
variance = np.var(data)#方差
std_dev = np.std(data)#标准差
range_value = np.ptp(data)#极差

    计算分位数
q1 = np.percentile(data, 25)
q3 = np.percentile(data, 75)
percentile_90 = np.percentile(data, 90)

    计算偏度
skewness = stats.skew(data)

    计算峰度
kurtosis = stats.kurtosis(data)

    计算相关系数
data1 = [1, 2, 3, 4, 5]
data2 = [2, 4, 6, 8, 10]
correlation = np.corrcoef(data1, data2)[0, 1]

    计算协方差
covariance = np.cov(data1, data2)[0, 1]

    计算累积和
cumulative_sum = np.cumsum(data)

    计算累积积
cumulative_product = np.cumprod(data)

    计算累积最大值和最小值
cumulative_max = np.maximum.accumulate(data)
cumulative_min = np.minimum.accumulate(data)

    计算累积平均值
cumulative_mean = np.cumsum(data) / np.arange(1, len(data) + 1)

    计算累积方差
cumulative_variance = np.cumsum((data - mean) ** 2) / np.arange(1, len(data) + 1)

    计算累积标准差
cumulative_std_dev = np.sqrt(cumulative_variance)


"""
import numpy as np
from scipy import stats


def moving_average(data, window_size):
    # 计算移动平均
    return [sum(data[i:i+window_size])/window_size for i in range(len(data)-window_size+1)]


def EWMA(data, alpha):
    # 计算指数加权移动平均（EWMA）
    ewma = [data[0]]
    for i in range(1, len(data)):
        ewma.append(alpha * data[i] + (1 - alpha) * ewma[-1])
    return ewma


def z_scores(data):
    # 计算列表元素的Z分数（标准分数）
    mean = np.mean(data)
    std_dev = np.std(data)
    return [(x - mean) / std_dev for x in data]


def CumulativeDistributionFunction(data):
    # 计算列表数据的累积密度函数（Cumulative Distribution Function, CDF）
    sorted_data = sorted(data)
    return [len(sorted_data[:i+1])/len(data) for i in range(len(data))]


def ProbabilityDensityFunction(data, bins=10):
    # 计算概率密度函数（Probability Density Function, PDF）
    histrogram, bin_edges = np.histogram(data, bins=bins, density=True)
    return histrogram


def rank_data(data):
    # 计算列表的排序索引
    sorted_data = sorted([(value, idx) for idx, value in enumerate(data)])
    return [idx for value, idx in sorted_data]


def count_inversions(data):
    # 计算列表的逆序对数量
    return sum(1 for i in range(len(data)) for j in range(i+1, len(data)) if data[i] > data[j])


def MAD(data):
    # 计算列表的中位数绝对偏差（MAD）
    median_val = np.median(data)
    return np.median(np.abs(data - median_val))


def M2(data):
    # 计算列表元素的二阶矩（M2）
    n = len(data)
    mean = np.mean(data)
    return sum((x - mean) ** 2 for x in data) / n


from math import log2
def entropy(data):
    # 计算信息熵
    unique_values = set(data)
    probabilities = [data.count(value) / len(data) for value in unique_values]
    return -sum(p * log2(p) for p in probabilities)



import pandas as pd
def auto_correlation(data, lag=1):
    # 计算列表的自动相关性
    series = pd.Series(data)
    return series.autocorr(lag)


def pearson_corr_matrix(data_list):
    # 计算Pearson相关系数矩阵
    df = pd.DataFrame(data_list)
    return df.corr()


from statsmodels.stats.outliers_influence import variance_inflation_factor
def jackknife_statistics(data):
    # 计算Jackknife统计量
    return [variance_inflation_factor(pd.Series(data), i) for i in range(len(data))]


def frequency_count(data):
    freq_dict = {}
    # 计算列表的元素频率
    for item in data:
        if item in freq_dict:
            freq_dict[item] += 1
        else:
            freq_dict[item] = 1
    return freq_dict


def frequency_distribution(data, bins=10):
    # 生成数据的频率分布表
    histogram, bin_edges = np.histogram(data, bins=bins)
    return histogram, bin_edges


def mad_ratio(data):
    # 计算列表的中位数绝对偏差比率（Median Absolute Deviation Ratio）
    median = np.median(data)
    mad = np.median(np.abs(data - median))
    return mad / np.std(data)


def linear_trend(data):
    # 检测列表中的线性趋势
    x = range(len(data))
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, data)
    return slope, intercept, r_value


def trimmed_mean(data, proportion=0.1):
    # 计算列表的三角矩（Trimmed Mean）
    sorted_data = sorted(data)
    trim_amnt = int(len(data) * proportion)
    trimmed_data = sorted_data[trim_amnt:-trim_amnt]
    return np.mean(trimmed_data)