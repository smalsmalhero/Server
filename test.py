import asyncio
import datetime

async def check_and_execute_task(target_date):
    while True:
        # 获取当前日期时间
        current_date = datetime.datetime.now()
        
        # 检查是否已到达目标日期时间
        if current_date >= target_date:
            # 执行任务
            print("执行指定任务！")
            break  # 任务执行后退出循环
        
        # 打印当前时间
        print("当前时间:", current_date)
        
        # 等待一段时间后再次检查
        await asyncio.sleep(1)  # 每秒检查一次

async def main(year, month, day, hour, minute):
    # 指定要执行任务的日期时间
    target_date = datetime.datetime(year, month, day, hour, minute, 0)  # 示例：2024年2月11日上午10点

    # 异步执行检查并执行任务
    await check_and_execute_task(target_date)

# 运行异步主函数
asyncio.run(main(2024,2,11,22,42))
