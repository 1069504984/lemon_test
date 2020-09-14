
# coding=utf-8
"""
拓展httprunner 的内置函数，
执行用例加载时，把此文件中的函数加到对应的debugtalk.py中，
以实现公共函数的效果
2019-08-16
"""
import hashlib
import hmac
import string
import time
import random
import datetime
import logging

SECRET_KEY = "DebugTalk"
logger = logging.getLogger(__name__)


def gen_random_string(str_len):
    return ''.join(
        random.choice(string.ascii_letters + string.digits) for _ in range(str_len))

def gen_md5(*str_args):
    return hashlib.md5("".join(str_args).encode('utf-8')).hexdigest()

def get_sign(*args):
    content = ''.join(args).encode('ascii')
    sign_key = SECRET_KEY.encode('ascii')
    sign = hmac.new(sign_key, content, hashlib.sha1).hexdigest()
    return sign

def remove_prefix(text, prefix):
    """ remove prefix from text
    """
    if text.startswith(prefix):
        return text[len(prefix):]
    return text

def get_date(days=0, separation='-'):
    """
    获取日期：默认返回8位当前日期，分割符为-
    :param days: 日期差，默认为0，整数类型，即当前日期。如为负数，即取之前n天日期；为正数，取之后日期
    :param separation:日期分割符，默认为减号，字符串类型。
    :return:
    """
    today = datetime.date.today()
    days = datetime.timedelta(days=days)
    target_date = today + days
    return target_date.strftime('%Y-%m-%d'.replace('-', separation))


def get_time(hours=0, minutes=0, seconds=0, separation=':'):
    """
    获取时间：默认返回6位当前时间，分割符为：， 如10:17:43
    :param hours: 小时差，默认为0，整数类型，即当前小时。如为负数，即取之前n个小时；为正数，取之后n个小时
    :param minutes:分钟差，默认为0，整数类型，即当前分钟。如为负数，即取之前n分钟；为正数，取之后n分钟
    :param seconds:秒差，默认为0，整数类型，即当前秒。如为负数，即取之前n秒；为正数，取之后n秒
    :param separation:时间分割符，默认为冒号，字符串类型。
    :return:
    """
    now = datetime.datetime.now()
    timedelta = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
    target_date = now + timedelta
    return target_date.strftime('%H:%M:%S'.replace(':', separation))


def get_datetime(days=0, hours=0, minutes=0, seconds=0, date_sep='-', time_sep=':', no_sep=False, start_date=None):
    """
    获取日期时间，默认为当前，格式：2019-08-28 10:41:35
    :param days: 日期差，默认为0，整数类型，即当前日期。如为负数，即取之前n天日期；为正数，取之后日期
    :param hours: 小时差，默认为0，整数类型，即当前小时。如为负数，即取之前n个小时；为正数，取之后n个小时
    :param minutes:分钟差，默认为0，整数类型，即当前分钟。如为负数，即取之前n分钟；为正数，取之后n分钟
    :param seconds:秒差，默认为0，整数类型，即当前秒。如为负数，即取之前n秒；为正数，取之后n秒
    :param date_sep:日期分割符，默认为减号，字符串类型。
    :param time_sep:时间分割符，默认为冒号，字符串类型。
    :param no_sep:是否带分割符，默认为False,即带分割符。如果为True,即返回无分割符的14位日期时间，且日期和时间分割符的设置也失效。
    :param start_date:指定开始时间点（格式:2019-08-28 10:41:35）, 默认为None，即开始时间点为当前日期时间，例子：
    如get_datetime(days=1, start_data="2019-08-28 10:41:35") 返回值为2019-08-29 10:41:35
    :return:
    """
    now = datetime.datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S") if start_date else datetime.datetime.now()
    timedelta = datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
    target_date = now + timedelta
    fmt = '%Y%m%d%H%M%S' if no_sep else '%Y-%m-%d %H:%M:%S'.replace('-', date_sep).replace(':', time_sep)
    return target_date.strftime(fmt)


def get_random_int(start=0, end=9):
    """
    获取随机整数,范围0-9， start >= end
    :param start:开始范围， 可为负数
    :param end:结束范围， 可为负数
    :return:
    """
    return random.randint(start, end)


def timestamp(unit='s'):
    """
    获取时间戳的字串
    默认返回秒，入参为’ms‘，返回毫秒
    :param unit:
    :return:
    """
    print('*' * 50, 'get time here')
    return str(time.time()).replace('.', '')[:[10, 13][unit == 'ms']]


def get_random_str(str_len, chartset=None, chartset_extend=None, first_chartset=None, first_len=1, prefix='',
                   suffix=''):
    """
    默认返回指定长度的英文大小写+数字+下划线组成的随机字串
    可选字符集选项：'en_L','en_U','num','province_sh','underline','sp_chars'
    :param str_len: 必填入参，字串长度
    :param chartset:重新定义默认适用字符集，以列表形式传入，如chartset=['en_L', 'num']
    :param chartset_extend:拓展默认适用字符集，以列表形式传入，如chartset_extend=['en_L', 'num']
    :param first_chartset:指定字串以什么字符集开头，如first_chartset='province_sh'（即以省份简称开头）
    :param first_len:指定的开头字符集的长度，占用随机长度。需配合first_chartset使用，未指定first_chartset，此入参无效果。
                    如first_len >= str_len，返回的字串将会是first_chartset所指定的字符集的first_len长度的随机字串。默认值为1
    :param prefix:传入指定字串，作为随机字串的前缀，不占用指定的随机字串长度
    :param suffix:传入指定字串，作为随机字串的后缀，不占用指定的随机字串长度
    :return:
    :author: zhangrongbin
    :date: 2019-8-19
    """
    chart_dict = {
        # 英文小写
        'en_L': string.ascii_lowercase,
        # 英文大写
        'en_U': string.ascii_uppercase,
        # 数字
        'num': string.digits,
        # 全国省份简称
        'province_sh': r'京津冀晋蒙辽吉黑沪苏浙皖闽赣鲁豫鄂湘粤桂琼渝川黔滇藏陕甘青宁新台港澳',
        # 下划线
        'underline': '_',
        # 英文特殊字符，包括下划线
        'sp_chars': string.punctuation
    }

    # 默认的应用字符集
    use_chartset = [
        chart_dict['en_L'], chart_dict['en_U'],
        chart_dict['num'], chart_dict['underline']
    ]
    # 重新定义字符集
    if chartset:
        use_chartset = []
        for cs in chartset:
            use_chartset.append(chart_dict[cs])

    # 拓展字符集
    if chartset_extend:
        for cs in chartset_extend:
            if chart_dict[cs] not in use_chartset:
                use_chartset.append(chart_dict[cs])

    chartset_str = ''.join(use_chartset)
    # 设置开头的字符
    if first_chartset:
        return prefix + ''.join(random.choice(chart_dict[first_chartset]) for _ in range(first_len)) + \
               ''.join(random.choice(chartset_str) for _ in range(str_len - first_len)) + suffix

    return prefix + ''.join(random.choice(chartset_str) for _ in range(str_len)) + suffix


def get_phone(ISP='all', prefix=None):
    """
    获取随机的11位手机号，可指定运营商号段，或使用自定义的前3位
    :param ISP: 运营商名字串， 默认为all，即全部运营商（号段），
        选项：yidong， liantong， dianxin， all（包括前三者）， simulate，
        如果指定了不存在的运营商字串，则返回取all
    :param prefix:可指定手机号前3位， 如设置了此入参，则ISP设置无效
    :return:
    """
    class ISPClass:
        """
        号段数据
        """
        yidong = [139, 138, 137, 136, 135, 134, 159, 158, 157, 150, 151, 152, 147, 188, 187, 182, 183, 184, 178]
        liantong = [130, 131, 132, 156, 155, 186, 185, 145, 176]
        dianxin = [133, 153, 189, 180, 181, 177, 173]
        simulate = [100, 199]
        all = yidong + liantong + dianxin

    if prefix:
        header = str(prefix)
    else:
        if hasattr(ISPClass, ISP):
            """
            获取指定运营商号段列表
            """
            choice_set = getattr(ISPClass, ISP)
            header = str(random.choice(choice_set))
        else:
            header = str(random.choice(ISPClass.all))

    return header + ''.join(str(random.randint(0, 9)) for _ in range(8))


def get_current_week_date(week_date, separation='-'):
    """
    获取本周（从周一开始）周一到周天的日期
    0代表周一，
    1代表周二，
    ...
    6代表周天
    :param separation:
    :param week_date:
    :return:
    """
    day = datetime.date.today()
    one_day = datetime.timedelta(days=1)
    if day.weekday() == week_date:
        # 今天为所求的礼拜日期
        return day
    elif day.weekday() > week_date:
        # 今天大于所求的礼拜日期，即所求时间已过去，要减日期
        while day.weekday() != week_date:
            day -= one_day
    elif day.weekday() < week_date:
        # 今天大于所求的礼拜日期，即所求时间未到，要加日期
        while day.weekday() != week_date:
            day += one_day
    return day.strftime('%Y-%m-%d'.replace('-', separation))


def get_current_month_start_or_end(flag='start', separation='-'):
    """
    返回本月1号日期和最后一天的日期
    :param flag:
    :param separation:
    :return:
    """
    now = datetime.datetime.now()
    month_start = datetime.datetime(now.year, now.month, 1)
    if now.month == 12:
        month_end = datetime.datetime(now.year, now.month, 31)
    else:
        month_end = datetime.datetime(now.year, now.month + 1, 1) - datetime.timedelta(days=1)
    return month_start.strftime('%Y-%m-%d'.replace('-', separation)) if flag == 'start' else month_end.strftime('%Y-%m-%d'.replace('-', separation))


def post_props(response, **kwargs):
    """
    用例传递当前请求中的变量/参数给后面的请求使用

    用法,分两步:
    1、在teardown_hooks中调用此函数。如果想传变量a=1,b=2
    则写成${post_props($response,a=1,b=2)}
    $response为必填，不能修改

    2、提取，在extract中提取传递的变量，即可传递给后面的请求使用
    因为传递的变量是附加在响应的headers中。所以提取路径为
    headers.变量名
    本例子则是
    headers.a
    和
    headers.b
    """
    response.headers.update(kwargs)


def get_the_attr_from_objList(obj_list, attr_by, attr_by_value, target_attr, attr_exclude=None, attr_exclude_value=None):
    """
    从对象列表中根据对象中某属性匹配指定对象，返回该对象中目标属性, 指定排除属性和值
    :param obj_list:对象列表，数据结构如[{}, {}, {}]
    :param attr_by:用于匹配对象的属性名
    :param attr_by_value:用于匹配对象属性名的值
    :param target_attr:目标属性名
    :param attr_exclude:用于排除对象的属性名
    :param attr_exclude_value:用例排除对象属性名的值, 多个值则使用英文逗号分割
    :return:
    """
    for obj in obj_list:
        # 排除属性和值均非空，且匹配。则跳过当前对象
        if attr_exclude and attr_exclude_value and obj[attr_exclude] in [x.strip() for x in attr_exclude_value.split(',')]:
            continue
        # 匹配属性命中，返回对象的目标属性
        if obj[attr_by]==attr_by_value:
            try:
                return obj[target_attr]
            except KeyError:
                return 'no match target_attr'

    return 'no match data'


def set_attr_to_objList(obj_list, new_attr_name, new_value, is_attr=True, attr_by=None, attr_by_value=None, attr_exclude=None, attr_exclude_value=None):
    """
    给对象添加新的属性，其值可以取对象其他的属性值，也可以由用户直接指定
    :param obj_list:对象列表，数据结构如[{}, {}, {}]
    :param new_attr_name:新添加的属性名
    :param new_value:用户指定的新值或对象属性名（取本对象中该属性的值作为新值）
    :param is_attr:是否取对象属性值
    :param attr_by:用于匹配对象的属性名
    :param attr_by_value:用于匹配对象属性名的值
    :param attr_exclude:用于排除对象的属性名
    :param attr_exclude_value:用例排除对象属性名的值, 多个值则使用英文逗号分割
    :return:
    """
    for obj in obj_list:
        # 排除属性和值均非空，且匹配。则跳过当前对象
        if attr_exclude and attr_exclude_value and obj[attr_exclude] in [x.strip() for x in attr_exclude_value.split(',')]:
            continue
        # 判断新属性的值来源于用户定义还是对象本身,为真则取对象本身中用户指定的值，否则取用户定义值
        new_attr_value = obj[new_value] if is_attr else new_value

        if attr_by and attr_by_value:
            if obj[attr_by]==attr_by_value:
                # 匹配属性命中,则添加新属性
                obj[new_attr_name] = new_attr_value
        else:
            # 未指定匹配的属性，全部对象添加新属性
            obj[new_attr_name] = new_attr_value
    return obj_list


def calculate(expression, decimal=None, data_type='str'):
    """
    数据计算，返回结果
    // 为整除；/ 为自然除法，如4/2=2.0；% 为求余数；其他参考python
    :param data_type:
    :param expression: 计算表达式，python表达式均可用，但建议只用于数据计算， 比如1+1
    :param decimal: 保存小数点位数，默认为None, 对结构是浮点数才有效，否则无效
    :data_type: 返回数据的类型，默认是str， 可选：int, str; 如果是浮点数据，则以str返回
    :return:
    """
    try:
        result = eval(expression) if decimal is None else round(eval(expression), decimal)
        if data_type not in ['str', 'int']:
            data_type = 'str'
        return eval("{}('{}')".format(data_type, result))
    except Exception:
        return 'expression error'


def get_half_HMS():
    """
    获取一天中全部的半小时的时间点，00：00：00至 23：30：00，共48个时间点，按升序以列表返回
    :return:
    """
    hms_list = []
    for h in range(24):
        h = str(h) if h >= 10 else "0{}".format(h)
        for m in ['00', '30']:
            hms_list.append("{}:{}:00".format(h, m))
    return hms_list


def get_next_half_HMS(num=1, start_hms=None):
    """
    获取当前或指定时间开始的第num个半小时的时间点
    :param num:获取的个数， 默认为1，直接返回下个半小时点的字串
    :param start_hms:指定开始的时间点，默认为None,即选当前时间。格式如“15：11：04”
    :return:
    """
    import re
    hms_list = get_half_HMS() * 2  # 解决跨天取值的问题
    hms_dict = list(enumerate(hms_list))  # [(0, '00:00:00')... (6, '03:00:00')...]

    start_hms = start_hms if start_hms is not None else get_time()
    if start_hms is not None:
        try:
            start_hms = re.search(r'.*(\d{2}:\d{2}:\d{2}).*', start_hms).group(1)
        except Exception:
            return '指定时间格式错误'
    else:
        start_hms = get_time()

    for hms in hms_dict:
        if hms[1] >= start_hms:
            start_index = hms[0]
            break
    else:
        start_index = 0

    return hms_dict[start_index+num-1][1]


def date_delta(start_str, end_str, format_str='%Y-%m-%d %H:%M:%S'):
    """
    计算日期差，返回整数日期差
    :param start_str: 开始时间串
    :param end_str: 结束时间串
    :param format_str: 时间串格式
    :return:
    """
    import datetime
    start = datetime.datetime.strptime(start_str, format_str)
    end = datetime.datetime.strptime(end_str, format_str)
    time_delta = end - start
    return time_delta.days


def wait_secs(n_secs):
    """
    时间等待
    :param n_secs: 秒数
    """
    time.sleep(n_secs)


def randomget(choices_list, target_attr=None, target_value=None):
    """
    随机获取某个匹配对象
    choices_list: 预期结构为[{}, {}]
    :param choices_list:
    :param target_attr:
    :param target_value:
    :return:
    """
    if len(choices_list) == 0:
        return 'no match data'
    if target_attr and target_value:
        new_choices_list = []
        for choice in choices_list:
            if choice.get(target_attr) == target_value:
                new_choices_list.append(choice)
        if len(new_choices_list):
            return random.choice(new_choices_list)
        return 'no match data'
    else:
        return random.choice(choices_list)


def collection_get(obj, attr, default=None):
    """
    从复杂的数据结构中提取字段数据
    :param obj: 数据
    :param attr: 字段路径, 列表/数组使用索引,字典使用key,多层路径以点连接.
    :param default:取值失败时,返回的默认值
    :return:字段数据
    """
    try:
        if '.' in attr:
            attr_path = attr.split('.')
            for a in attr_path:
                obj = obj[int(a)] if str.isdigit(a) else obj.get(a)
                # 如果obj为None,则当前a是不存在的key
                if obj is None:
                    raise Exception('路径错误,{}不存在'.format(a))
            # 遍历到最后,此即为目标取值
            return obj
        else:
            return obj[int(attr)] if str.isdigit(attr) else obj.get(attr, default)
    except Exception as e:
        logger.error('数据获取失败，{}'.format(e))
        return default or str(e)

if __name__ == '__main__':
    pass
