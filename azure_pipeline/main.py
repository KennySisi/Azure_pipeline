import json

def lambda_handler(event, context):
    # 从事件中获取两个数字
    number1 = event.get('number1', 17)
    number2 = event.get('number2', 14)

    # 计算两个数字的和
    result = number1 + number2

    # 构造返回的 JSON 数据
    response = {
        'statusCode': 200,
        'body': json.dumps({'result': result})
    }

    return response
