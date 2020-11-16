from test1 import Test1
import time


def round(name):
    start = time.time()
    test = Test1()
    test.setup_method(1)
    url = test.test_1(name)
    test.teardown_method(1)
    # test.get_one_app_privacy_text(url)
    end = time.time()
    print('Running time: %s Seconds' % (end - start))
    return url


name = input('请输入一个安卓app的名字：')
print('程序正在运行中')
round(name)
print('程序运行完毕，您所需要的隐私政策文件在本级目录下')
user_input_str = input('请输入exit退出:')
if user_input_str == 'exit':
    exit()
