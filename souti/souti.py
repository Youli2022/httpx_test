import httpx
from urllib.parse import quote


class TikuQuery:
    def __init__(self):
        self.token = "fcecac7fe95546f0be74de934b886e9c"  # 请确保此token有效
        self.query_url = "https://tk.enncy.cn/query"
        self.info_url = "https://tk.enncy.cn/info"

    def query_question(self, question):
        """查询题目答案（自动编码题目）"""
        try:
            # 对题目进行URL编码
            encoded_question = quote(question)
            params = {
                'token': self.token,
                'title': encoded_question
            }

            r = httpx.get(self.query_url, params=params, timeout=10)
            data = r.json()

            # 调试用 - 打印原始响应
            print(f"调试信息 - 原始响应: {data}")

            if data.get('code') == 1:
                result = data.get('data', {})
                return {
                    'success': True,
                    'question': result.get('question', question),
                    'answer': result.get('answer', '未找到答案'),
                    'times': result.get('times', 0),
                    'message': data.get('message', '请求成功')
                }
            else:
                # 检查是否是token错误
                if data.get('message') == '无效的token':
                    return {
                        'success': False,
                        'message': '❌ Token无效，请更新token',
                        'times': 0
                    }
                return {
                    'success': False,
                    'message': data.get('message', '题库中没有找到匹配答案'),
                    'times': data.get('data', {}).get('times', 0),
                    'suggestion': '请尝试：\n1. 检查题目是否完整准确\n2. 更换题目表述方式'
                }

        except httpx.RequestError as e:
            return {
                'success': False,
                'message': f'网络请求失败: {str(e)}'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'处理错误: {str(e)}'
            }

    # [...] 其余代码保持不变（pretty_print和主循环）

    def get_tk_info(self):
        """获取题库信息"""
        params = {
            'token': self.token
        }

        try:
            r = httpx.get(self.info_url, params=params)
            data = r.json()

            if not isinstance(data, dict):
                return {
                    'success': False,
                    'message': 'API返回格式不正确'
                }

            if data.get('code') == 1:
                result = data.get('data', {})
                return {
                    'success': True,
                    'times': result.get('times', '未知'),
                    'user_times': result.get('user_times', '未知'),
                    'success_times': result.get('success_times', '未知'),
                    'message': data.get('message', '请求成功')
                }
            else:
                return {
                    'success': False,
                    'message': data.get('message', '请求失败')
                }

        except httpx.RequestError as e:
            return {
                'success': False,
                'message': f"网络请求错误: {str(e)}"
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"处理响应时出错: {str(e)}"
            }


def pretty_print(result):
    """美化输出结果"""
    if result['success']:
        if 'question' in result:
            print("\n✅ 查询成功")
            print(f"📝 题目: {result['question']}")
            print(f"📌 答案: {result['answer']}")
            print(f"🔢 剩余查询次数: {result['times']}")
        else:
            print("\n📊 题库信息")
            print(f"🔄 剩余查询次数: {result['times']}")
            print(f"📈 题库使用总次数: {result['user_times']}")
            print(f"✅ 成功查询次数: {result['success_times']}")
    else:
        print("\n❌ 操作失败")
        print(f"⚠️ 错误信息: {result['message']}")
        if 'times' in result and result['times'] != '未知':
            print(f"🔢 剩余查询次数: {result['times']}")


if __name__ == '__main__':
    tiku = TikuQuery()

    while True:
        print("\n📚 题库查询系统")
        print("1. 题目查询")
        print("2. 题库信息查询")
        print("3. 退出")

        choice = input("请选择功能(1/2/3): ").strip()

        if choice == '1':
            question = input("请输入要查询的题目: ").strip()
            if not question:
                print("⚠️ 题目不能为空！")
                continue

            result = tiku.query_question(question)
            pretty_print(result)

        elif choice == '2':
            result = tiku.get_tk_info()
            pretty_print(result)

        elif choice == '3':
            print("👋 感谢使用，再见！")
            break

        else:
            print("⚠️ 无效的选择，请重新输入！")