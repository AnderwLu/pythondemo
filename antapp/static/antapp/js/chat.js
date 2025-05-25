const model = document.querySelector('#model');
let url = model.value;
fetch(url);
model.onchange = e => {
    url = e.target.value;
    // 将选择的值存储到 localStorage
    localStorage.setItem('selectedModel', url);
    window.location.reload();
};

// 页面加载时检查并恢复选择的值
if (localStorage.getItem('selectedModel')) {
    url = localStorage.getItem('selectedModel');
    model.value = url;
    fetch(url);
}

// 获取form
const form = document.querySelector('form');
const textArea = document.querySelector('textarea');

textArea.onkeydown = e => {
    if (e.key === 'Enter' && !e.shiftKey && !e.ctrlKey && !e.altKey) {
        e.preventDefault();
        form.dispatchEvent(new Event('submit'));
    }
};

// 添加CSS动画（如果还没有）
if (!document.getElementById('blinking-cursor-style')) {
    const style = document.createElement('style');
    style.id = 'blinking-cursor-style';
    style.textContent = `
        @keyframes blink {
            from, to { opacity: 1; }
            50% { opacity: 0; }
        }
        .cursor-blink {
            display: inline-block;
            margin-left: 2px;
            font-weight: bold;
            animation: blink 1s step-end infinite;
            position: absolute;
            pointer-events: none;
            z-index: 100;
            mix-blend-mode: difference;
            color: white;
        }
    `;
    document.head.appendChild(style);
}

// 创建光标元素
const cursorSpan = document.createElement('span');
cursorSpan.className = 'cursor-blink';
cursorSpan.textContent = '|';

// 光标控制相关函数
function findLastTextNode(element) {
    if (element.nodeType === 3) return element; // 文本节点

    let lastTextNode = null;
    for (let i = element.childNodes.length - 1; i >= 0; i--) {
        const node = element.childNodes[i];
        const textNode = findLastTextNode(node);
        if (textNode) return textNode;
    }
    return null;
}

function showCursor(contentDom) {
    const lastTextNode = findLastTextNode(contentDom);

    if (lastTextNode) {
        // 获取最后一个文本节点的位置
        const range = document.createRange();
        range.selectNodeContents(lastTextNode);
        range.collapse(false); // 将范围折叠到末尾

        // 获取位置
        const rect = range.getBoundingClientRect();

        // 设置光标位置
        cursorSpan.style.left = `${rect.right}px`;
        cursorSpan.style.top = `${rect.top}px`;

        // 添加光标到DOM（如果还没有添加）
        if (!cursorSpan.parentNode) {
            document.body.appendChild(cursorSpan);
        }
    } else {
        // 如果没有文本节点，将光标定位到contentDom的开始位置
        const rect = contentDom.getBoundingClientRect();

        // 设置光标位置到内容区域的左上角
        cursorSpan.style.left = `${rect.left}px`;
        cursorSpan.style.top = `${rect.top}px`;

        // 添加光标到DOM
        if (!cursorSpan.parentNode) {
            document.body.appendChild(cursorSpan);
        }
    }
}

function hideCursor() {
    if (cursorSpan.parentNode) {
        cursorSpan.remove();
    }
}

form.onsubmit = async e => {
    e.preventDefault();
    const content = textArea.value;

    // 立即清空缩略图和重置文件输入框
    const preview = document.querySelector('.img-preview');
    preview.innerHTML = ''; // 清空预览区

    createUserContent('鲁');
    const robot = createRobotContent();

    // 在robot元素的content区域
    const contentDom = robot.getContentDom();

    // 在发送请求前先显示光标，让用户知道正在处理
    showCursor(contentDom);

    // 构造 FormData
    const formData = new FormData();
    formData.append('content', content);

    // 获取所有图片文件并添加到 formData
    const files = document.querySelector('.img-upload').files;
    for (let i = 0; i < files.length; i++) {
        formData.append('images', files[i]); // 后端用 images 字段接收
    }

    // fetch 提交
    const resp = await fetch(url + '/', {
        method: 'POST',
        body: formData
    });
    // 重置文件输入框
    const fileInput = document.querySelector('.img-upload');
    fileInput.value = ''; // 直接清空值

    // 流式读取
    const reader = resp.body.getReader();
    const decoder = new TextDecoder();

    // 确保光标可见 - 这是为了防止在请求和读取之间有任何光标被移除的情况
    if (!cursorSpan.parentNode) {
        document.body.appendChild(cursorSpan);
    }

    // 缓存上一次处理的文本，用于增量渲染
    let lastText = '';
    let updateCursorTimeout = null;

    while (1) {
        const { done, value } = await reader.read();
        if (done) {
            // 响应结束时隐藏光标
            hideCursor();
            break;
        }

        // 解码新的数据块
        const newText = decoder.decode(value, { stream: true });

        // 只追加新文本，而不是每次都重新渲染整个内容
        robot.appendChunk(newText);

        // 清除之前的超时
        if (updateCursorTimeout) {
            clearTimeout(updateCursorTimeout);
        }

        // 设置一个新的超时，减少光标更新频率
        updateCursorTimeout = setTimeout(() => {
            showCursor(contentDom);
        }, 50); // 50ms延迟，减少闪烁

        // 确保滚动到底部
        document.documentElement.scrollTo(0, document.documentElement.scrollHeight);
    }

    // 确保响应完成后移除光标
    hideCursor();

    robot.over();
};
