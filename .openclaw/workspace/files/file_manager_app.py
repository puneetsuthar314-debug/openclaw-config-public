#!/root/anaconda3/bin/python3
"""
简易文件管理 Web 界面
功能：浏览、上传、下载、删除文件
"""

from flask import Flask, request, send_file, send_from_directory, jsonify, render_template_string
from urllib.parse import quote
import os
import werkzeug

app = Flask(__name__)

# 添加 urlencode 过滤器到模板
@app.template_filter('urlencode')
def urlencode_filter(s):
    return quote(str(s), safe='')

# 工作空间根目录
WORKSPACE_ROOT = '/root/.openclaw/workspace'
# 待处理文件目录
PENDING_DIR = '/root/.openclaw/workspace/pending_uploads'

# HTML 模板
VIEW_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>查看文件 - {{ filename }}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, monospace;
            background: #f5f5f5;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .header h1 { font-size: 20px; }
        .btn {
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            text-decoration: none;
            display: inline-block;
        }
        .btn-back {
            background: rgba(255,255,255,0.2);
            color: white;
        }
        .btn-back:hover { background: rgba(255,255,255,0.3); }
        .content {
            padding: 20px 30px;
        }
        .file-content {
            background: #f8f9fa;
            border: 1px solid #e0e0e0;
            border-radius: 4px;
            padding: 20px;
            white-space: pre-wrap;
            word-wrap: break-word;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 14px;
            line-height: 1.6;
            max-height: 70vh;
            overflow: auto;
            color: #333;
        }
        .alert {
            padding: 15px 30px;
            background: #f8d7da;
            color: #721c24;
            border-bottom: 1px solid #f5c6cb;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📄 {{ filename | e }}</h1>
            <div>
                {% if back_path %}
                <a href="/browse?path={{ back_path | urlencode }}" class="btn btn-back">← 返回</a>
                {% else %}
                <a href="/" class="btn btn-back">← 返回首页</a>
                {% endif %}
            </div>
        </div>
        {% if error %}
        <div class="alert">{{ error }}</div>
        {% else %}
        <div class="content">
            <div class="file-content">{{ content | e }}</div>
        </div>
        {% endif %}
    </div>
</body>
</html>
'''

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>文件管理器 - OpenClaw</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f5;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .header h1 { font-size: 24px; }
        .upload-section {
            padding: 20px 30px;
            border-bottom: 1px solid #e0e0e0;
            background: #fafafa;
        }
        .upload-form {
            display: flex;
            gap: 10px;
            align-items: center;
        }
        .upload-form input[type="file"] {
            flex: 1;
            padding: 10px;
            border: 2px dashed #667eea;
            border-radius: 4px;
            background: white;
        }
        .btn {
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.3s;
        }
        .btn-primary {
            background: #667eea;
            color: white;
        }
        .btn-primary:hover { background: #5568d3; }
        .btn-danger {
            background: #e74c3c;
            color: white;
            padding: 5px 10px;
            font-size: 12px;
        }
        .btn-danger:hover { background: #c0392b; }
        .btn-download {
            background: #27ae60;
            color: white;
            padding: 5px 10px;
            font-size: 12px;
            margin-right: 5px;
            text-decoration: none;
            border-radius: 4px;
        }
        .btn-download:hover { background: #229954; }
        .breadcrumb {
            padding: 15px 30px;
            background: #f8f9fa;
            border-bottom: 1px solid #e0e0e0;
        }
        .breadcrumb a {
            color: #667eea;
            text-decoration: none;
        }
        .breadcrumb a:hover { text-decoration: underline; }
        .file-list {
            padding: 20px 30px;
        }
        .file-item {
            display: flex;
            align-items: center;
            padding: 12px;
            border-bottom: 1px solid #f0f0f0;
            transition: background 0.2s;
        }
        .file-item:hover { background: #f8f9fa; }
        .file-icon {
            font-size: 24px;
            margin-right: 15px;
            width: 30px;
            text-align: center;
        }
        .file-info {
            flex: 1;
        }
        .file-name {
            font-weight: 500;
            color: #333;
        }
        .file-meta {
            font-size: 12px;
            color: #888;
            margin-top: 4px;
        }
        .file-actions {
            display: flex;
            gap: 8px;
        }
        .empty-state {
            text-align: center;
            padding: 60px 20px;
            color: #888;
        }
        .alert {
            padding: 15px 30px;
            background: #d4edda;
            color: #155724;
            border-bottom: 1px solid #c3e6cb;
        }
        .alert-error {
            background: #f8d7da;
            color: #721c24;
            border-bottom: 1px solid #f5c6cb;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📁 文件管理器</h1>
            <div>工作空间：{{ workspace_root }}</div>
        </div>
        
        {% if message %}
        <div class="alert">{{ message }}</div>
        {% endif %}
        {% if error %}
        <div class="alert alert-error">{{ error }}</div>
        {% endif %}
        
        <div class="upload-section">
            <form class="upload-form" method="POST" action="/upload" enctype="multipart/form-data">
                <input type="file" name="file" multiple required>
                <select name="target_dir" style="padding: 10px; border: 2px solid #667eea; border-radius: 4px;">
                    <option value="">当前目录</option>
                    <option value="pending_uploads">📥 待处理文件夹</option>
                </select>
                <button type="submit" class="btn btn-primary">⬆️ 上传文件</button>
            </form>
        </div>
        
        <div class="breadcrumb">
            📍 当前位置：
            {% for part in breadcrumbs %}
                {% if loop.last %}
                    <strong>{{ part.name | e }}</strong>
                {% else %}
                    <a href="/browse?path={{ part.path | urlencode }}">{{ part.name | e }}</a> /
                {% endif %}
            {% endfor %}
            <span style="margin-left: 20px;">
                <a href="/browse?path=pending_uploads" style="color: #e74c3c; font-weight: bold;">📥 待处理文件夹</a>
            </span>
        </div>
        
        <div class="file-list">
            {% if parent_path %}
            <div class="file-item">
                <div class="file-icon">📤</div>
                <div class="file-info">
                    <div class="file-name"><a href="/browse?path={{ parent_path | urlencode }}" style="color: #667eea; text-decoration: none;">返回上级目录</a></div>
                </div>
            </div>
            {% endif %}
            
            {% for folder in folders %}
            <div class="file-item">
                <div class="file-icon">📁</div>
                <div class="file-info">
                    <div class="file-name"><a href="/browse?path={{ folder.path | urlencode }}" style="color: #667eea; text-decoration: none;">{{ folder.name | e }}</a></div>
                    <div class="file-meta">{{ folder.files }} 个文件</div>
                </div>
            </div>
            {% endfor %}
            
            {% for file in files %}
            <div class="file-item">
                <div class="file-icon">{{ file.icon }}</div>
                <div class="file-info">
                    <div class="file-name">{{ file.name | e }}</div>
                    <div class="file-meta">{{ file.size }} | {{ file.modified }}</div>
                </div>
                <div class="file-actions">
                    {% if file.viewable %}
                    <a href="/view?path={{ file.path | urlencode }}" class="btn btn-download" style="background: #3498db;">👁️ 查看</a>
                    {% endif %}
                    <a href="/download?path={{ file.path | urlencode }}" class="btn btn-download">⬇️ 下载</a>
                    <form method="POST" action="/delete" style="display: inline;" onsubmit="return confirm('确定要删除 {{ file.name | e }} 吗？');">
                        <input type="hidden" name="path" value="{{ file.path }}">
                        <button type="submit" class="btn btn-danger">🗑️ 删除</button>
                    </form>
                </div>
            </div>
            {% endfor %}
            
            {% if folders|length == 0 and files|length == 0 %}
            <div class="empty-state">
                <div style="font-size: 48px; margin-bottom: 20px;">📭</div>
                <div>此目录为空</div>
            </div>
            {% endif %}
        </div>
    </div>
</body>
</html>
'''

def get_file_icon(filename):
    """根据文件扩展名返回图标"""
    ext = os.path.splitext(filename)[1].lower()
    icons = {
        '.pdf': '📄', '.doc': '📝', '.docx': '📝', '.txt': '📃',
        '.jpg': '🖼️', '.jpeg': '🖼️', '.png': '🖼️', '.gif': '🖼️', '.svg': '🖼️',
        '.mp4': '🎬', '.mov': '🎬', '.avi': '🎬', '.mkv': '🎬',
        '.mp3': '🎵', '.wav': '🎵', '.flac': '🎵',
        '.zip': '📦', '.tar': '📦', '.gz': '📦', '.rar': '📦',
        '.py': '🐍', '.js': '📜', '.html': '🌐', '.css': '🎨',
        '.json': '📋', '.xml': '📋', '.md': '📖',
    }
    return icons.get(ext, '📄')

# 可查看的文件扩展名
VIEWABLE_EXTENSIONS = ['.txt', '.md', '.py', '.js', '.json', '.xml', '.html', '.css', '.csv', '.log', '.sh', '.yml', '.yaml', '.toml', '.ini', '.cfg', '.conf']

def is_viewable(filename):
    """检查文件是否可以在线查看"""
    ext = os.path.splitext(filename)[1].lower()
    return ext in VIEWABLE_EXTENSIONS

def format_size(size_bytes):
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"

def get_breadcrumbs(path):
    """生成面包屑导航"""
    parts = []
    current = ''
    for part in path.strip('/').split('/'):
        current = os.path.join(current, part)
        parts.append({'name': part, 'path': current})
    return parts

@app.route('/')
def index():
    return browse()

@app.route('/browse')
def browse():
    path = request.args.get('path', '')
    full_path = os.path.join(WORKSPACE_ROOT, path)
    
    # 安全检查：确保路径在工作空间内
    if not os.path.abspath(full_path).startswith(os.path.abspath(WORKSPACE_ROOT)):
        return render_template_string(HTML_TEMPLATE, 
            workspace_root=WORKSPACE_ROOT,
            breadcrumbs=[{'name': '🏠 根目录', 'path': ''}],
            folders=[], files=[],
            message='', error='❌ 禁止访问工作空间外的目录')
    
    if not os.path.exists(full_path):
        return render_template_string(HTML_TEMPLATE,
            workspace_root=WORKSPACE_ROOT,
            breadcrumbs=[{'name': '🏠 根目录', 'path': ''}],
            folders=[], files=[],
            message='', error='❌ 目录不存在')
    
    if not os.path.isdir(full_path):
        return render_template_string(HTML_TEMPLATE,
            workspace_root=WORKSPACE_ROOT,
            breadcrumbs=[{'name': '🏠 根目录', 'path': ''}],
            folders=[], files=[],
            message='', error='❌ 这不是一个目录，无法浏览')
    
    # 获取目录内容
    try:
        entries = os.listdir(full_path)
    except PermissionError:
        return render_template_string(HTML_TEMPLATE,
            workspace_root=WORKSPACE_ROOT,
            breadcrumbs=[{'name': '🏠 根目录', 'path': ''}],
            folders=[], files=[],
            message='', error='❌ 无权限访问此目录')
    
    folders = []
    files = []
    
    for entry in sorted(entries):
        entry_path = os.path.join(full_path, entry)
        rel_path = os.path.join(path, entry) if path else entry
        
        if os.path.isdir(entry_path):
            try:
                file_count = len(os.listdir(entry_path))
            except PermissionError:
                file_count = 0
            folders.append({
                'name': entry,
                'path': rel_path,
                'files': file_count
            })
        else:
            try:
                stat = os.stat(entry_path)
                files.append({
                    'name': entry,
                    'path': rel_path,
                    'size': format_size(stat.st_size),
                    'modified': f"{stat.st_mtime:.0f}",
                    'icon': get_file_icon(entry),
                    'viewable': is_viewable(entry)
                })
            except Exception as e:
                # 跳过无法访问的文件
                pass
    
    # 生成面包屑
    breadcrumbs = [{'name': '🏠 根目录', 'path': ''}]
    breadcrumbs.extend(get_breadcrumbs(path))
    
    # 上级目录路径
    parent_path = os.path.dirname(path) if path else None
    
    return render_template_string(HTML_TEMPLATE,
        workspace_root=WORKSPACE_ROOT,
        breadcrumbs=breadcrumbs,
        folders=folders,
        files=files,
        parent_path=parent_path,
        message='', error='')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return browse()
    
    files = request.files.getlist('file')
    target_dir = request.form.get('target_dir', '')
    uploaded = 0
    
    for file in files:
        if file.filename:
            # 确定保存目录
            if target_dir == 'pending_uploads':
                save_dir = PENDING_DIR
            else:
                path = request.args.get('path', '')
                save_dir = os.path.join(WORKSPACE_ROOT, path)
            
            # 安全检查
            if not os.path.abspath(save_dir).startswith(os.path.abspath(WORKSPACE_ROOT)):
                continue
            
            # 确保目录存在
            os.makedirs(save_dir, exist_ok=True)
            
            file.save(os.path.join(save_dir, file.filename))
            uploaded += 1
    
    message = f'✅ 成功上传 {uploaded} 个文件' if uploaded > 0 else ''
    return browse()

@app.route('/download')
def download():
    path = request.args.get('path', '')
    full_path = os.path.join(WORKSPACE_ROOT, path)
    
    # 安全检查
    if not os.path.abspath(full_path).startswith(os.path.abspath(WORKSPACE_ROOT)):
        return '禁止访问', 403
    
    if not os.path.exists(full_path) or os.path.isdir(full_path):
        return '文件不存在', 404
    
    return send_file(full_path, as_attachment=True)

@app.route('/view')
def view():
    path = request.args.get('path', '')
    full_path = os.path.join(WORKSPACE_ROOT, path)
    
    # 安全检查
    if not os.path.abspath(full_path).startswith(os.path.abspath(WORKSPACE_ROOT)):
        return render_template_string(VIEW_TEMPLATE, error='❌ 禁止访问工作空间外的目录', content='')
    
    if not os.path.exists(full_path) or os.path.isdir(full_path):
        return render_template_string(VIEW_TEMPLATE, error='❌ 文件不存在', content='')
    
    filename = os.path.basename(full_path)
    if not is_viewable(filename):
        return render_template_string(VIEW_TEMPLATE, error='❌ 不支持预览此文件类型', content='')
    
    try:
        # 检查文件大小，限制最大 1MB
        file_size = os.path.getsize(full_path)
        if file_size > 1024 * 1024:  # 1MB
            return render_template_string(VIEW_TEMPLATE, 
                error=f'❌ 文件过大（{format_size(file_size)}），仅支持预览 1MB 以内的文件', 
                content='', filename=filename, back_path=path)
        
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        try:
            with open(full_path, 'r', encoding='gbk') as f:
                content = f.read()
        except:
            return render_template_string(VIEW_TEMPLATE, 
                error='❌ 无法读取文件内容（可能是二进制文件）', 
                content='', filename=filename, back_path=path)
    except Exception as e:
        return render_template_string(VIEW_TEMPLATE, 
            error=f'❌ 读取失败：{str(e)}', 
            content='', filename=filename, back_path=path)
    
    return render_template_string(VIEW_TEMPLATE, error='', content=content, filename=filename, back_path=path)

@app.route('/delete', methods=['POST'])
def delete():
    path = request.args.get('path', '') or request.form.get('path', '')
    full_path = os.path.join(WORKSPACE_ROOT, path)
    
    # 安全检查
    if not os.path.abspath(full_path).startswith(os.path.abspath(WORKSPACE_ROOT)):
        return '禁止访问', 403
    
    if not os.path.exists(full_path):
        return '文件不存在', 404
    
    try:
        if os.path.isdir(full_path):
            os.rmdir(full_path)
        else:
            os.remove(full_path)
    except Exception as e:
        return f'删除失败：{str(e)}', 500
    
    return browse()

if __name__ == '__main__':
    print("🚀 文件管理器启动中...")
    print(f"📁 工作空间：{WORKSPACE_ROOT}")
    print("🌐 访问地址：http://0.0.0.0:8888")
    print("按 Ctrl+C 停止服务")
    app.run(host='0.0.0.0', port=8888, debug=True)
