# -*- coding: utf-8 -*-
"""
心理评估报告生成API服务器
提供完整的API接口服务
"""

import os
import json
import threading
import queue
import tempfile
import shutil
import socket
from flask import Flask, request, jsonify, send_file, send_from_directory
from datetime import datetime
import sys
import time
import uuid
import glob

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入报告生成模块和数据生成器
from generate_complete_report import generate_complete_report_from_json
from data_generator import create_mock_data

app = Flask(__name__)

# 任务队列
task_queue = queue.Queue()
# 结果存储
results = {}
# 任务状态
task_status = {}

# 存储模拟数据的目录
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'api_data')

def get_local_ip():
    """获取本机IP地址"""
    try:
        # 创建一个UDP socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 连接到一个外部地址（不会真正发送数据）
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def cleanup_python_cache():
    """清理Python缓存文件"""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 清理__pycache__目录
        pycache_dirs = glob.glob(os.path.join(current_dir, '**', '__pycache__'), recursive=True)
        for pycache_dir in pycache_dirs:
            try:
                shutil.rmtree(pycache_dir)
                print(f"✓ 已清理缓存目录: {os.path.relpath(pycache_dir, current_dir)}")
            except Exception as e:
                print(f"✗ 清理缓存目录失败: {pycache_dir} - {e}")
        
        # 清理.pyc文件
        pyc_files = glob.glob(os.path.join(current_dir, '**', '*.pyc'), recursive=True)
        for pyc_file in pyc_files:
            try:
                os.remove(pyc_file)
                print(f"✓ 已清理缓存文件: {os.path.relpath(pyc_file, current_dir)}")
            except Exception as e:
                print(f"✗ 清理缓存文件失败: {pyc_file} - {e}")
        
        if pycache_dirs or pyc_files:
            print(f"缓存清理完成，共清理 {len(pycache_dirs)} 个目录和 {len(pyc_files)} 个文件")
        
    except Exception as e:
        print(f"清理Python缓存时出错: {e}")

def auto_cleanup_task_files(task_dir):
    """自动清理单个任务的中间文件，只保留最终报告"""
    try:
        if not os.path.exists(task_dir):
            return 0
        
        cleaned_count = 0
        for filename in os.listdir(task_dir):
            file_path = os.path.join(task_dir, filename)
            
            # 保留最终报告文件
            if (filename.endswith('_心理评估报告.html') or 
                filename.endswith('_complete_report.json')):
                continue
            
            # 删除其他文件（中间数据、临时文件等）
            try:
                os.remove(file_path)
                cleaned_count += 1
            except Exception:
                pass  # 静默处理删除失败
        
        return cleaned_count
        
    except Exception:
        return 0

def cleanup_all_intermediate_files():
    """清理所有任务的中间文件，保留最终报告"""
    try:
        project_root = os.path.dirname(os.path.abspath(__file__))
        api_results_dir = os.path.join(project_root, 'api_results')
        total_cleaned = 0
        
        if not os.path.exists(api_results_dir):
            return total_cleaned
        
        for task_dir_name in os.listdir(api_results_dir):
            task_path = os.path.join(api_results_dir, task_dir_name)
            if os.path.isdir(task_path):
                cleaned_count = auto_cleanup_task_files(task_path)
                total_cleaned += cleaned_count
        
        if total_cleaned > 0:
            print(f"✓ 清理完成，共清理 {total_cleaned} 个中间文件")
        
        return total_cleaned
        
    except Exception as e:
        print(f"清理中间文件时出错: {e}")
        return 0

def process_json_data(json_data, task_id):
    """处理JSON数据并生成报告"""
    try:
        # 提取record_id
        record_id = json_data.get('data', {}).get('recordId', 'unknown')
        
        # 修改fileList中的https链接为http
        if 'data' in json_data and 'fileList' in json_data['data']:
            for file_info in json_data['data']['fileList']:
                if 'file_address' in file_info:
                    file_info['file_address'] = file_info['file_address'].replace('https://', 'http://')
        
        # 在项目目录下创建输出目录
        project_root = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(project_root, 'api_results', f'task_{task_id}')
        os.makedirs(output_dir, exist_ok=True)
        
        # 保存JSON数据到输出目录（临时文件）
        json_file_path = os.path.join(output_dir, f'{task_id}.txt')
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        
        print(f"[Task {task_id}] 处理数据文件: {record_id}")
        
        # 调用报告生成函数
        output_file = generate_complete_report_from_json(
            json_file_path,
            output_dir=output_dir,
            cleanup_temp_files=True,  # 自动清理临时音频文件
            task_id=task_id
        )
        
        if output_file and os.path.exists(output_file):
            # 读取生成的报告
            with open(output_file, 'r', encoding='utf-8') as f:
                report_content = f.read()
            
            # 自动清理中间文件，只保留最终报告
            auto_cleanup_task_files(output_dir)
            
            # 统计最终文件
            final_files = []
            for filename in os.listdir(output_dir):
                file_path = os.path.join(output_dir, filename)
                if os.path.isfile(file_path):
                    final_files.append({
                        'filename': filename,
                        'size': os.path.getsize(file_path)
                    })
            
            print(f"[Task {task_id}] ✓ 报告生成完成，保留 {len(final_files)} 个最终文件")
            
            # 保存结果
            results[task_id] = {
                'status': 'completed',
                'record_id': record_id,
                'report': report_content,
                'output_file': output_file,
                'output_dir': output_dir,
                'final_files': final_files,
                'timestamp': datetime.now().isoformat()
            }
            task_status[task_id] = 'completed'
            
        else:
            results[task_id] = {
                'status': 'failed',
                'record_id': record_id,
                'error': '报告生成失败',
                'output_dir': output_dir,
                'timestamp': datetime.now().isoformat()
            }
            task_status[task_id] = 'failed'
            
    except Exception as e:
        results[task_id] = {
            'status': 'failed',
            'record_id': record_id if 'record_id' in locals() else 'unknown',
            'error': str(e),
            'output_dir': output_dir if 'output_dir' in locals() else None,
            'timestamp': datetime.now().isoformat()
        }
        task_status[task_id] = 'failed'

def worker():
    """后台工作线程"""
    while True:
        try:
            task_id, json_data = task_queue.get(timeout=1)
            task_status[task_id] = 'processing'
            process_json_data(json_data, task_id)
            task_queue.task_done()
        except queue.Empty:
            continue
        except Exception as e:
            print(f"Worker error: {e}")
            continue

# 启动后台工作线程
worker_thread = threading.Thread(target=worker, daemon=True)
worker_thread.start()

@app.route('/data/<filename>')
def get_data(filename):
    """提供模拟数据"""
    try:
        file_path = os.path.join(DATA_DIR, filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=False, mimetype='application/json')
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api_results/<task_id>/<filename>')
def serve_result_file(task_id, filename):
    """提供api_results目录下的文件访问"""
    try:
        project_root = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(project_root, 'api_results', f'task_{task_id}', filename)
        
        if os.path.exists(file_path):
            # 根据文件扩展名设置MIME类型
            if filename.endswith('.html'):
                return send_file(file_path, mimetype='text/html')
            elif filename.endswith('.json'):
                return send_file(file_path, mimetype='application/json')
            else:
                return send_file(file_path)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/submit', methods=['POST'])
def submit_task():
    """提交任务"""
    try:
        json_data = request.get_json()
        if not json_data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # 生成任务ID
        task_id = str(uuid.uuid4())
        
        # 添加到任务队列
        task_queue.put((task_id, json_data))
        task_status[task_id] = 'queued'
        
        return jsonify({
            'task_id': task_id,
            'status': 'queued',
            'message': 'Task submitted successfully'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/status/<task_id>', methods=['GET'])
def get_task_status(task_id):
    """查询任务状态"""
    try:
        if task_id not in task_status:
            return jsonify({'error': 'Task not found'}), 404
        
        status = task_status[task_id]
        response = {
            'task_id': task_id,
            'status': status
        }
        
        if task_id in results:
            result = results[task_id]
            response['timestamp'] = result.get('timestamp')
            if status == 'failed':
                response['error'] = result.get('error')
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download/<task_id>', methods=['GET'])
def download_result(task_id):
    """下载处理结果（返回输出目录中的所有文件）"""
    try:
        if task_id not in results:
            return jsonify({'error': 'Task not found'}), 404
        
        result = results[task_id]
        if result['status'] != 'completed':
            return jsonify({'error': 'Task not completed or failed'}), 400
        
        output_dir = result.get('output_dir')
        if not output_dir or not os.path.exists(output_dir):
            return jsonify({'error': 'Output directory not found'}), 404
        
        # 获取输出目录中的所有文件
        files = []
        for filename in os.listdir(output_dir):
            file_path = os.path.join(output_dir, filename)
            if os.path.isfile(file_path):
                files.append({
                    'filename': filename,
                    'size': os.path.getsize(file_path),
                    'download_url': f'/api/download/{task_id}/{filename}'
                })
        
        return jsonify({
            'task_id': task_id,
            'record_id': result['record_id'],
            'files': files
        })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download/<task_id>/<filename>', methods=['GET'])
def download_file(task_id, filename):
    """下载指定文件"""
    try:
        if task_id not in results:
            return jsonify({'error': 'Task not found'}), 404
        
        result = results[task_id]
        output_dir = result.get('output_dir')
        
        if not output_dir or not os.path.exists(output_dir):
            return jsonify({'error': 'Task directory not found'}), 404
        
        file_path = os.path.join(output_dir, filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True, download_name=filename)
        else:
            return jsonify({'error': 'File not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/clean/<task_id>', methods=['DELETE'])
def clean_task(task_id):
    """清理任务和临时文件"""
    try:
        cleaned_items = []
        
        if task_id == 'intermediate':
            # 清理所有任务的中间文件，保留最终报告
            cleaned_count = cleanup_intermediate_files()
            cleaned_items.append(f'清理中间文件: {cleaned_count} 个')
            
        elif task_id == 'cache':
            # 清理Python缓存文件
            cleanup_python_cache()
            cleaned_items.append('Python缓存文件')
            
        elif task_id in results:
            # 清理特定任务
            result = results[task_id]
            output_dir = result.get('output_dir')
            
            # 删除输出目录
            if output_dir and os.path.exists(output_dir):
                shutil.rmtree(output_dir)
                cleaned_items.append(f'输出目录: {output_dir}')
            
            # 清理内存中的结果
            del results[task_id]
            cleaned_items.append(f'任务结果: {task_id}')
            
            if task_id in task_status:
                del task_status[task_id]
                cleaned_items.append(f'任务状态: {task_id}')
        else:
            return jsonify({'error': 'Task not found'}), 404
        
        return jsonify({
            'message': 'Cleaning completed successfully',
            'cleaned_items': cleaned_items
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    """根路径 - 显示API信息"""
    local_ip = get_local_ip()
    port = 5000
    
    api_info = {
        "service": "心理评估报告生成API",
        "version": "2.0",
        "status": "running",
        "server_ip": local_ip,
        "server_port": port,
        "endpoints": {
            "submit_task": f"http://{local_ip}:{port}/api/submit",
            "check_status": f"http://{local_ip}:{port}/api/status/<task_id>",
            "download_result": f"http://{local_ip}:{port}/api/download/<task_id>",
            "download_file": f"http://{local_ip}:{port}/api/download/<task_id>/<filename>",
            "clean_task": f"http://{local_ip}:{port}/api/clean/<task_id>",
            "get_data": f"http://{local_ip}:{port}/data/<filename>"
        },
        "sample_data": {
            "10001.txt": f"http://{local_ip}:{port}/data/10001.txt",
            "10002.txt": f"http://{local_ip}:{port}/data/10002.txt"
        },
        "usage": {
            "1": "POST JSON data to /api/submit to get task_id",
            "2": "GET /api/status/<task_id> to check processing status",
            "3": "GET /api/download/<task_id> to download completed report",
            "4": "DELETE /api/clean/<task_id> to clean up task files",
            "5": "DELETE /api/clean/cache to clean Python cache files"
        }
    }
    
    return jsonify(api_info)

if __name__ == '__main__':
    print("🚀 启动心理评估报告生成API服务器...")
    print("=" * 50)
    
    # 启动时清理Python缓存文件
    print("🧹 启动时清理...")
    cleanup_python_cache()
    
    # 可选：清理旧的中间文件（保留最终报告）
    try:
        import sys
        if '--clean-intermediate' in sys.argv:
            print("🗂️ 清理旧的中间文件...")
            cleaned_count = cleanup_all_intermediate_files()
            if cleaned_count > 0:
                print(f"清理完成，处理了 {cleaned_count} 个中间文件")
            else:
                print("没有需要清理的中间文件")
    except Exception as e:
        print(f"清理中间文件时出错: {e}")
    
    # 创建模拟数据
    print("\n正在创建模拟数据...")
    create_mock_data()
    
    # 获取本机IP
    local_ip = get_local_ip()
    port = 5000
    
    print(f"\n📡 API服务器信息:")
    print(f"  服务地址: http://{local_ip}:{port}")
    print(f"  API文档: http://{local_ip}:{port}/")
    print(f"  示例数据: http://{local_ip}:{port}/data/10001.txt")
    print(f"  示例数据: http://{local_ip}:{port}/data/10002.txt")
    print(f"\n🧹 清理命令:")
    print(f"  中间文件: curl -X DELETE http://{local_ip}:{port}/api/clean/intermediate")
    print(f"  Python缓存: curl -X DELETE http://{local_ip}:{port}/api/clean/cache")
    print(f"\n💡 启动参数:")
    print(f"  --clean-intermediate: 启动时清理中间文件")
    print("\n" + "=" * 50)
    print("\n服务器启动中...\n")
    
    # 启动Flask应用
    app.run(host='0.0.0.0', port=port, debug=False)