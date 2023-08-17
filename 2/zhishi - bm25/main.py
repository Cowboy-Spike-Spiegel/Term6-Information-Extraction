from process import *
from search import *

if __name__ == '__main__':
    print("加载数据...")
    text_list = get_text_list()
    print("构建向量...")
    bag, count = get_bag(text_list)
    count = csr_matrix(count)  # 转换为稀疏矩阵
    print("生成索引（此步可能较慢，请耐心等待）...")
    inverse_index = generate_inverse_index(text_list, bag, count)
    print("成功！请输入查找内容：")
    while True:
        search_str = input("> ")

        if search_str == 'q':
            print("感谢您的使用！")
            exit(0)

        result = run_search(search_str, inverse_index, files, text_list, bag, count)
        flag = True
        for i in result:
            print(i)
            s = input("输入：n 展示下一项, 输入：q 关闭, 输入：g 推荐此结果, 输入：d 不推荐此结果\n> ")
            if s == 'q':
                print("已关闭！请输入新的查找内容：（或输入：q 退出）")
                flag = False
                break
            else:
                continue
        if flag:
            print("没有更多结果了！请输入新的查找内容：（或输入：q 退出）")
