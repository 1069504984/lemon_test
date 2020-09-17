import os
import io
import logging
import json
import re
from datetime import datetime
# from PIL import Image
import yaml
from django.conf import settings
from httprunner.task import HttpRunner
from httprunner.exceptions import ParamsError
from rest_framework import status
from rest_framework.response import Response

from testcases.models import Testcases
from envs.models import Envs
from reports.models import Reports
from debugtalks.models import DebugTalks
from configures.models import Configures
from projects.models import Projects
from  interfaces.models import  Interfaces
logger = logging.getLogger('test')


def timestamp_to_datetime(summary, type=True):
    if not type:
        time_stamp = int(summary["time"]["start_at"])
        summary['time']['start_datetime'] = datetime. \
            fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')

    for detail in summary['details']:
        try:
            time_stamp = int(detail['time']['start_at'])
            detail['time']['start_at'] = datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
        except Exception:
            pass

        for record in detail['records']:
            try:
                time_stamp = int(record['meta_data']['request']['start_timestamp'])
                record['meta_data']['request']['start_timestamp'] = \
                    datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
            except Exception:
                pass
    return summary


def bytes2str(data):
    """
    如果data中包含有bytes类型数据，在使用JsonResponse时会报错
    函数用于把请求响应中的bytes转成str
    :param data:字典类型
    :return:
    """
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, bytes):
                data[key] = value.decode()
            elif isinstance(value, dict):
                data[key] = bytes2str(value)

            elif isinstance(value, list):
                for i in range(len(value)):
                    value[i] = bytes2str(value[i])
                data[key] = value
    elif isinstance(data, list):
        for i in range(len(data)):
            data[i] = bytes2str(data[i])
    return data

def second2hms(second):
    """
    把秒数转换成时分秒格式
    :param second:
    :return:
    """
    second = float(second)

    h = int(second / 3600)
    second = second % 3600

    m = int(second / 60)
    s = round(second % 60, 2)

    t = str(s) + 's'
    if m:
        t = '{0}m {1}s'.format(str(m), str(s))
    if h:
        t = '{0}h {1}m {2}s'.format(str(h), str(m), str(s))

    return t

# def thumbnail(path, new_path=None, q=100):
#     '''压缩并保存到文件'''
#     img = Image.open(path)
#     w, h = img.size
#     width, height = w * q // 100, h * q // 100
#     img.thumbnail((width, height))
#
#     if new_path:
#         img.save(new_path, img.format)
#     else:
#         img.save(path, img.format)

def generate_testcase_files(instance, env, testcase_dir_path):
    testcases_list = []
    config = {
        'config': {
            'name': instance.name,
            'request': {
                'base_url': env.base_url if env else ''
            }
        }
    }
    testcases_list.append(config)

    # include = eval(instance.include)
    # request = eval(instance.request)
    # 获取当前用例的前置配置和前置用例
    include = json.loads(instance.include, encoding='utf-8')
    # 获取当前用例的请求信息
    request = json.loads(instance.request, encoding='utf-8')

    interface_name = instance.interface.name  # 接口名称
    project_name = instance.interface.project.name  # 项目名称

    testcase_dir_path = os.path.join(testcase_dir_path, project_name)
    # 创建项目名所在文件夹
    if not os.path.exists(testcase_dir_path):
        os.makedirs(testcase_dir_path)
        debugtalk_obj = DebugTalks.objects.filter(project__name=project_name).first()
        if debugtalk_obj:
            debugtalk = debugtalk_obj.debugtalk
        else:
            debugtalk = ""

        # 读取公共函数
        with open(os.path.join(settings.BASE_DIR, 'httprunner_extend_functions.py'), encoding='utf-8') as f:
            code = f.read()
        file_content = code + '\n' + debugtalk
        # 创建debugtalk.py文件
        with open(os.path.join(testcase_dir_path, 'debugtalk.py'),
                  mode='w',
                  encoding='utf-8') as one_file:
            one_file.write(debugtalk)

    testcase_dir_path = os.path.join(testcase_dir_path, interface_name)
    # 在项目目录下创建接口名所在文件夹
    if not os.path.exists(testcase_dir_path):
        os.makedirs(testcase_dir_path)

    # {'config': 2, 'testcases': [2,5]}
    # 如果include前置中有config, 那么添加到testcases_list中
    if 'config' in include:
        config_id = include.get('config')
        config_obj = Configures.objects.filter(id=config_id).first()
        if config_obj:
            # 需要将请求头(当前为嵌套字典的列表), 需要转化为字典
            # config_request = eval(config_obj.request)
            config_request = json.loads(config_obj.request, encoding='utf-8')

            # config_request = eval(config_obj.request)
            # config_request.get('config').get('request').setdefault('base_url', env.base_url)
            # config_dict = config_request.get('config')
            # config_dict['request']['base_url'] = env.base_url
            # config_request['config']['name'] = instance.name
            config_request['config']['request']['base_url'] = env.base_url  # 添加公共配置的公共url
            # testcases_list.append(config_request)
            testcases_list[0] = config_request   # 覆盖原有的请求配置

    # 如果include前置中有testcases, 那么添加到testcases_list中
    if 'testcases' in include:
        for t_id in include.get('testcases'):
            testcase_obj = Testcases.objects.filter(id=t_id).first()
            if testcase_obj:
                try:
                    # testcase_request = eval(testcase_obj.request)
                    testcase_request = json.loads(testcase_obj.request, encoding='utf-8')
                except Exception as e:
                    logger.error(e)
                    continue
                else:
                    testcases_list.append(testcase_request)

    # 将当前用例的request添加到testcases_list
    testcases_list.append(request)

    with open(os.path.join(testcase_dir_path, instance.name + '.yml'),
              mode="w", encoding="utf-8") as one_file:
        yaml.dump(testcases_list, one_file, allow_unicode=True)





def generate_debug_files(instance, env, testcase_dir_path):
    testcases_list = []
    config = {
        'config': {
            'name': '',
            'request': {
                'base_url': env.base_url if env else ''
            }
        }
    }
    testcases_list.append(config)

    # include = eval(instance.include)
    # request = eval(instance.request)
    # 获取当前用例的前置配置和前置用例
    include = json.loads(instance.get("include"), encoding='utf-8')
    # 获取当前用例的请求信息
    request = json.loads(instance.get("request"), encoding='utf-8')

    interface_name = Interfaces.objects.get(id=instance.get('interface').get("iid")).name # 接口名称
    project_name = Projects.objects.get(id=instance.get("interface").get("pid")).name # 项目名称

    testcase_dir_path = os.path.join(testcase_dir_path, project_name)
    # 创建项目名所在文件夹
    if not os.path.exists(testcase_dir_path):
        os.makedirs(testcase_dir_path)
        debugtalk_obj = DebugTalks.objects.filter(project__name=project_name).first()
        if debugtalk_obj:
            debugtalk = debugtalk_obj.debugtalk
        else:
            debugtalk = ""
        # 读取公共函数
        with open(os.path.join(settings.BASE_DIR, 'httprunner_extend_functions.py'), encoding='utf-8') as f:
            code = f.read()
        file_content = code + '\n' + debugtalk
        # 创建debugtalk.py文件
        with open(os.path.join(testcase_dir_path, 'debugtalk.py'),
                  mode='w',
                  encoding='utf-8') as one_file:
            one_file.write(file_content)

    testcase_dir_path = os.path.join(testcase_dir_path, interface_name)
    # 在项目目录下创建接口名所在文件夹
    if not os.path.exists(testcase_dir_path):
        os.makedirs(testcase_dir_path)

    # {'config': 2, 'testcases': [2,5]}
    # 如果include前置中有config, 那么添加到testcases_list中
    if 'config' in include:
        config_id = include.get('config')
        config_obj = Configures.objects.filter(id=config_id).first()
        if config_obj:
            config_request = json.loads(config_obj.request, encoding='utf-8')
            config_request['config']['request']['base_url'] = env.base_url  # 添加公共配置的公共url
            testcases_list[0] = config_request

    # 如果include前置中有testcases, 那么添加到testcases_list中
    if 'testcases' in include:
        for t_id in include.get('testcases'):
            testcase_obj = Testcases.objects.filter(id=t_id).first()
            if testcase_obj:
                try:
                    testcase_request = json.loads(testcase_obj.request, encoding='utf-8')
                except Exception as e:
                    logger.error(e)
                    continue
                else:
                    testcases_list.append(testcase_request)

    # 将当前用例的request添加到testcases_list
    testcases_list.append(request)

    with open(os.path.join(testcase_dir_path, instance.get("name") + '.yml'),
              mode="w", encoding="utf-8") as one_file:
        yaml.dump(testcases_list, one_file, allow_unicode=True)

def create_report(runner, report_name=None):

    """
    创建测试报告
    :param runner:
    :param report_name:
    :return:
    """
    time_stamp = int(runner.summary["time"]["start_at"])
    start_datetime = datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
    runner.summary['time']['start_datetime'] = start_datetime
    # duration保留3位小数
    runner.summary['time']['duration'] = round(runner.summary['time']['duration'], 3)
    report_name = report_name if report_name else start_datetime
    runner.summary['html_report_name'] = report_name

    for item in runner.summary['details']:
        try:
            for record in item['records']:
                record['meta_data']['response']['content'] = record['meta_data']['response']['content']
                record['meta_data']['response']['cookies'] = dict(record['meta_data']['response']['cookies'])

                request_body = record['meta_data']['request'].get('body')
                if request_body is None:
                    continue
                if "files" in record['meta_data']['request'].keys():
                    record['meta_data']['request'].pop("files")
                    if "body" in record['meta_data']['request'].keys():
                            record['meta_data']['request'].pop("body")


        except Exception as e:
            continue
    summary = bytes2str(runner.summary)
    summary['top10error'], summary['successes'], summary['failures'], summary['errors'] = top10error(summary)
    summary = json.dumps(summary, ensure_ascii=False)
    # 添加top10错误表数据及其他统计数据

    report_name = report_name + '_' + datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')
    report_path = runner.gen_html_report(html_report_name=report_name)

    with open(report_path, encoding='utf-8') as stream:
        reports = stream.read()

    test_report = {
        'name': report_name,
        'result': runner.summary.get('success'),
        'success': runner.summary.get('stat').get('successes'),
        'count': runner.summary.get('stat').get('testsRun'),
        'html': reports,
        'summary': summary
    }
    report_obj = Reports.objects.create(**test_report)
    return report_obj.id

def top10error(summary):
    pattern = r'(.*\.)?(.*?Error:(?:.*?Failure)?)(.+)'  # 提取错误原因正则表格式
    successes = 0
    failures = 0
    errors = 0
    top10errors = {}
    for item in summary['details']:
        # 提取用例执行情况
        if item['success']:
            successes += 1
        else:
            if item['stat']['errors'] > 0:
                errors += 1
            else:
                failures += 1
            # 对错误用例原因统计
            for record in item['records']:
                if record['status'] != 'success':
                    all_list = re.findall(pattern, record['attachment'])
                    m = all_list[-1]  # 取最后一个报错原因
                    if top10errors.get(m[1]):
                        # 已记录本错误原因
                        top10errors[m[1]][0] += 1
                    else:
                        # 未记录本错误原因
                        top10errors[m[1]] = [1, m[2]]  # [errorNum, errorDetail]
                    break  # 只取每个用例中第一个报错请求

    # 计算各错误率
    wrong_total = failures + errors
    for key, value in top10errors.items():
        # [errorNum, errorDetail, errorRate]
        top10errors[key].append('%.2f' % (value[0] / wrong_total * 100) + '%')

    # 错误原因排序
    # [('errorName', [errorNum, errorDetail, errorRate])...]
    top10errors = sorted(top10errors.items(), key=lambda x: x[1][0], reverse=True)[:10]  # 取前10，不足10，取全部

    data_list = []
    for item in top10errors:
        data_list.append({
            'err_name': item[0],
            'err_sum': item[1][0],
            'err_rate': item[1][2],
            'err_detail': item[1][1]
        })

    return data_list, successes, failures, errors

def run_testcase(instance, testcase_dir_path,debug=False):
    """
    运行用例
    :return:
    :param instance: 实例
    :param testcase_dir_path: 用例根目录路径
    :return dict
    """
    runner = HttpRunner()
    # runner.run(testcase_dir_path)
    try:
        runner.run(testcase_dir_path)
    except ParamsError:
        logger.error("用例参数有误")
        data = {
            "msg": "用例参数有误"
        }
        return Response(data, status=400)

    runner.summary = timestamp_to_datetime(runner.summary, type=False)
    # 运行用例
    # 原内容为字节类型不能序列化,需要转换。转换后作为响应返回前端
    summary = bytes2str(runner.summary)
    try:
        report_name = instance.name
    except Exception as e:
        report_name = '被遗弃的报告' + '-' + datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')
    if debug == True :
        return summary
    else:
        report_id = create_report(runner, report_name=report_name)
        data_dict = {
            "id": report_id
        }

        return Response(data_dict, status=status.HTTP_201_CREATED)

def python2js(value, check_list=(None, True, False)):
    """
    把check_list中的值从python类型转成js(json)类型，以适配前端显示
    :param value:
    :param check_list:
    :return:
    """
    if check_list is not None and value in check_list:
        value = json.dumps(value)
    else:
        value = str(value)
    return value

def tidy_tree_data(data, tree_list, parent_path=None):
    '''
    此函数为递归函数, 用于整理返回给前端显示的树形结果数据
    初始的data为响应数据response，是字典类型
    所以初始化数据不能是字典或列表以外的类型
    :parent_path：为None即表示为顶层。子层向下传入时应该把当前parent_path+本身路径(key)
    :param data:
    :param tree_list:传入要保存数据的列表，建议传[]（适配ztree框架的数据要求）
    :return:
    '''
    if isinstance(data, list):
        for i, v in enumerate(data):
            '''
            假设响应数据如下：
            [
                {
                    "id": 53,
                    "title": "xxxxxxxxxx",
                    "content": "<p>123</p>",
                    "author": "123",
                    "pub_date": "2019-07-24T13:45:33.755000"
                },
                {
                    "id": 54,
                    "title": "324",
                    "content": "<p>234</p>",
                    "author": "234",
                    "pub_date": "2019-07-24T13:45:44.484000"
                }
            ]
            如果想取出第一条数据的id,httprunner提取数据，则使用json.0.id
            所以在前端做结果树形显示时，把列表数据的索引作为一级，也是为了后面做数据自动提取作铺垫。
            '''
            # 保存本次节点数据的字典对象
            node = {}
            if isinstance(v, (str, int, float, bool)):
                node['title'] = str(i) + '-->' + python2js(v)
                node['expect'] = v
            else:
                node['title'] = i
                sub_parent_path = str(i) if parent_path is None else parent_path + '.' + str(i) # 下一层的父路径
                node['children'] = tidy_tree_data(v, [], parent_path=sub_parent_path)
            # 保存本数据节点的路径(父路径.本节点路径)
            node['path'] = str(i) if parent_path is None else parent_path + '.' + str(i)
            node['name'] = i
            if node:
                tree_list.append(node)
    elif isinstance(data, dict):
        for key, value in data.items():
            if key in ['content_type', 'content_size', 'response_time_ms', 'elapsed_ms']:
                # 这三个字段在httprunner中不支持提取，所以过滤掉。
                continue
            # 保存本次节点数据的字典对象
            node = {}
            # 下一层的父路径
            sub_parent_path = key if parent_path is None else parent_path + '.' + key
            if isinstance(value, (list, dict, tuple)):
                # 列表或字典 递归解释
                node['children'] = tidy_tree_data(value, [], parent_path=sub_parent_path)
                node['title'] = key if node['children'] else key + '-->' + python2js(value)
            else:
                if key in ['text', 'content']:
                    '''
                    text类型为字节和 content类型为字串，但是为了适配前端显示，把这两字段的内容解释成功字典或列表
                    如果解释失败，有可以是内容为空，或者包含不可解释成python对象的内容。
                    此时直接按字串输出
                    '''
                    try:
                        value = re.sub(r':\s*null\s*,', ': None,', value if isinstance(value, str) else value.decode())
                        value = eval(value)
                        # node['name'] = key
                        if isinstance(value, (list, dict)):
                            node['children'] = tidy_tree_data(value, [], parent_path=sub_parent_path)
                            node['title'] = key if node['children'] else key + '-->[]'
                        else:
                            node['title'] = key + '-->' + python2js(value)
                            node['expect'] = value
                    except Exception:
                        node['title'] = key + '-->' + python2js(value)
                        node['expect'] = value
                else:
                    # 字串直接输出
                    node['title'] = key + '-->' + python2js(value)
                    node['expect'] = value
            # 保存本数据节点的路径(父路径.本节点路径)
            node['path'] = key if parent_path is None else parent_path + '.' + key
            node['name'] = key
            if node:
                tree_list.append(node)
    return tree_list
