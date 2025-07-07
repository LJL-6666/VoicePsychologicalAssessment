#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
心理评估API测试客户端
模拟数据传输并保存结果
"""

import requests
import json
import time
import os
import sys

def get_api_base_url():
    """获取API基础URL"""
    # 首先尝试获取API信息
    try:
        response = requests.get('http://localhost:5000/', timeout=5)
        if response.status_code == 200:
            info = response.json()
            server_ip = info['server_ip']
            return f'http://{server_ip}:5000'
    except:
        pass
    
    # 如果失败，使用默认值
    return 'http://localhost:5000'

def test_api_workflow():
    """测试完整的API工作流程"""
    base_url = get_api_base_url()
    print(f"API基础URL: {base_url}")
    print("=" * 60)
    
    # 1. 获取API信息
    print("1. 获取API信息...")
    try:
        response = requests.get(f'{base_url}/')
        info = response.json()
        print(f"   服务: {info['service']}")
        print(f"   本地IP: {info['server_ip']}")
        print(f"   示例数据: ")
        for url in info['sample_data']:
            print(f"     - {url}")
    except Exception as e:
        print(f"   错误: {e}")
        return
    
    print("\n" + "=" * 60)
    
    # 2. 获取模拟数据并提交任务
    task_ids = []
    data_files = ['10001.txt', '10002.txt']
    
    for filename in data_files:
        print(f"\n2. 处理数据文件: {filename}")
        
        # 获取数据
        print(f"   获取数据...")
        try:
            response = requests.get(f'{base_url}/data/{filename}')
            response.raise_for_status()
            json_data = response.json()
            record_id = json_data['data']['recordId']
            print(f"   成功获取数据，RecordId: {record_id}")
        except Exception as e:
            print(f"   获取数据失败: {e}")
            continue
        
        # 提交任务
        print(f"   提交任务...")
        try:
            response = requests.post(
                f'{base_url}/api/submit',
                json=json_data,
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()
            result = response.json()
            task_id = result['task_id']
            task_ids.append(task_id)
            print(f"   任务提交成功，Task ID: {task_id}")
        except Exception as e:
            print(f"   提交任务失败: {e}")
            if response:
                print(f"   响应: {response.text}")
            continue
    
    if not task_ids:
        print("\n没有成功提交的任务")
        return
    
    print("\n" + "=" * 60)
    
    # 3. 监控任务状态
    print("\n3. 监控任务状态...")
    completed_tasks = []
    max_wait_time = 300  # 最多等待5分钟
    start_time = time.time()
    
    while len(completed_tasks) < len(task_ids):
        if time.time() - start_time > max_wait_time:
            print("   超时：任务处理时间过长")
            break
        
        for task_id in task_ids:
            if task_id in completed_tasks:
                continue
            
            try:
                response = requests.get(f'{base_url}/api/status/{task_id}')
                status_data = response.json()
                status = status_data['status']
                
                if status == 'completed':
                    completed_tasks.append(task_id)
                    print(f"   任务 {task_id} 已完成")
                elif status == 'failed':
                    completed_tasks.append(task_id)
                    print(f"   任务 {task_id} 失败: {status_data.get('error', '未知错误')}")
                else:
                    print(f"   任务 {task_id} 状态: {status}", end='\r')
                
            except Exception as e:
                print(f"   查询状态失败 {task_id}: {e}")
        
        if len(completed_tasks) < len(task_ids):
            time.sleep(2)  # 等待2秒后再次查询
    
    print("\n" + "=" * 60)
    
    # 4. 下载结果
    print("\n4. 下载结果文件...")
    
    # 创建结果保存目录
    results_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'api_results')
    os.makedirs(results_dir, exist_ok=True)
    
    for task_id in task_ids:
        print(f"\n   处理任务 {task_id} 的结果:")
        
        try:
            # 获取文件列表
            response = requests.get(f'{base_url}/api/download/{task_id}')
            if response.status_code != 200:
                print(f"   获取文件列表失败: {response.json().get('error', '未知错误')}")
                continue
            
            file_info = response.json()
            record_id = file_info['record_id']
            files = file_info['files']
            
            print(f"   RecordId: {record_id}")
            print(f"   文件数量: {len(files)}")
            
            # 创建任务目录
            task_dir = os.path.join(results_dir, f'task_{task_id}')
            os.makedirs(task_dir, exist_ok=True)
            
            # 分类并下载每个文件
            final_reports = []
            intermediate_files = []
            
            for file_data in files:
                filename = file_data['filename']
                file_url = f"{base_url}/api/download/{task_id}/{filename}"
                
                print(f"   下载: {filename}")
                try:
                    response = requests.get(file_url)
                    response.raise_for_status()
                    
                    # 保存文件
                    file_path = os.path.join(task_dir, filename)
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    
                    # 分类文件
                    if filename.endswith('_心理评估报告.html') or filename.endswith('_complete_report.json'):
                        final_reports.append(filename)
                        print(f"     📄 最终报告保存到: {file_path}")
                    else:
                        intermediate_files.append(filename)
                        print(f"     🗂️ 中间文件保存到: {file_path}")
                    
                except Exception as e:
                    print(f"     下载失败: {e}")
            
            # 显示文件分类信息
            if final_reports:
                print(f"   📄 最终报告文件: {len(final_reports)} 个")
            if intermediate_files:
                print(f"   🗂️ 中间数据文件: {len(intermediate_files)} 个 [可清理]")
            
            print(f"   任务 {task_id} 结果已保存")
                
        except Exception as e:
            print(f"   处理结果失败: {e}")
    
    print("\n" + "=" * 60)
    print(f"\n完成！结果保存在: {results_dir}")
    
    # 显示保存的文件
    print("\n保存的文件：")
    all_final_reports = []
    all_intermediate_files = []
    
    for task_id in task_ids:
        task_dir = os.path.join(results_dir, f'task_{task_id}')
        if os.path.exists(task_dir):
            print(f"\n任务 {task_id}:")
            for filename in os.listdir(task_dir):
                file_path = os.path.join(task_dir, filename)
                file_size = os.path.getsize(file_path)
                
                if filename.endswith('_心理评估报告.html') or filename.endswith('_complete_report.json'):
                    print(f"  📄 {filename} ({file_size:,} bytes)")
                    all_final_reports.append((task_id, filename, file_path))
                else:
                    print(f"  🗂️ {filename} ({file_size:,} bytes) [可清理]")
                    all_intermediate_files.append((task_id, filename, file_path))
    
    # 自动清理本地中间文件
    if all_intermediate_files:
        print("\n🧹 自动清理本地中间文件...")
        total_cleaned = 0
        for task_id in task_ids:
            task_dir = os.path.join(results_dir, f'task_{task_id}')
            cleaned_count = cleanup_local_intermediate_files(task_dir)
            total_cleaned += cleaned_count
        print(f"本地清理完成，共清理 {total_cleaned} 个中间文件")
        
        # 询问是否清理服务器文件
        print("\n清理服务器文件选项:")
        print("1. 清理服务器中间文件")
        print("2. 清理服务器Python缓存")
        print("3. 跳过服务器清理")
        
        try:
            choice = input("\n请选择 (1-3): ").strip()
            
            if choice == '1':
                print("\n清理服务器中间文件...")
                cleanup_server_files(None, base_url, 'intermediate')
                
            elif choice == '2':
                print("\n清理服务器Python缓存...")
                cleanup_server_files(None, base_url, 'cache')
                
            elif choice == '3':
                print("\n跳过服务器清理")
                print(f"如需手动清理，请调用: DELETE {base_url}/api/clean/intermediate")
                
            else:
                print("\n无效选择，跳过清理")
                
        except KeyboardInterrupt:
            print("\n\n用户取消，跳过清理")
        except Exception as e:
            print(f"\n清理过程中出错: {e}")

def cleanup_local_intermediate_files(save_dir):
    """清理本地下载的中间文件，保留最终报告"""
    try:
        if not os.path.exists(save_dir):
            return 0
        
        cleaned_count = 0
        for filename in os.listdir(save_dir):
            file_path = os.path.join(save_dir, filename)
            
            # 保留重要的最终报告文件
            if (filename.endswith('_心理评估报告.html') or 
                filename.endswith('_complete_report.json')):
                continue
            
            # 删除中间数据文件
            try:
                os.remove(file_path)
                cleaned_count += 1
            except Exception:
                pass  # 静默处理删除失败
        
        return cleaned_count
    except Exception:
        return 0

def cleanup_server_files(task_id, base_url, clean_type='intermediate'):
    """清理服务器文件"""
    try:
        # 构建清理URL
        cleanup_url = f"{base_url}/api/clean/{task_id or 'global'}"
        
        # 发送清理请求
        response = requests.post(cleanup_url, json={'type': clean_type}, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('status') == 'success':
                print(f"✓ {result.get('message', '服务器清理完成')}")
                return True
        
        print(f"✗ 服务器清理失败: HTTP {response.status_code}")
        return False
            
    except Exception as e:
        print(f"✗ 服务器清理异常: {e}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("心理评估API测试客户端")
    print("=" * 60)
    
    # 检查API服务是否运行
    print("\n检查API服务...")
    try:
        response = requests.get('http://localhost:5000/', timeout=5)
        if response.status_code == 200:
            print("✓ API服务正在运行")
        else:
            print("✗ API服务响应异常")
            sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("✗ 无法连接到API服务")
        print("  请先运行: python api_server.py")
        sys.exit(1)
    except Exception as e:
        print(f"✗ 检查失败: {e}")
        sys.exit(1)
    
    print("\n开始测试...")
    try:
        test_api_workflow()
    except KeyboardInterrupt:
        print("\n\n测试中断")
    except Exception as e:
        print(f"\n\n测试失败: {e}")
        import traceback
        traceback.print_exc()