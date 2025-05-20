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

form.onsubmit = async e => {
    e.preventDefault();
    const content = textArea.value;

    // 立即清空缩略图和重置文件输入框
    const preview = document.querySelector('.img-preview');
    preview.innerHTML = ''; // 清空预览区

    createUserContent('鲁');
    const robot = createRobotContent();

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
            }
        `;
        document.head.appendChild(style);
    }

    // 在robot元素的content区域添加一个专门的光标容器
    const contentDom = robot.getContentDom();
    const cursorSpan = document.createElement('span');
    cursorSpan.className = 'cursor-blink';
    cursorSpan.textContent = '|';
    contentDom.appendChild(cursorSpan);

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

    // 添加光标显示/隐藏函数
    function showCursor() {
        if (!cursorSpan.parentNode) {
            contentDom.appendChild(cursorSpan);
        }
    }

    function hideCursor() {
        if (cursorSpan.parentNode) {
            cursorSpan.remove();
        }
    }

    // 初始显示光标
    showCursor();

    // 缓存上一次处理的文本，用于增量渲染
    let lastText = '';

    while (1) {
        const { done, value } = await reader.read();
        if (done) {
            // 响应结束时隐藏光标
            hideCursor();
            break;
        }

        // 解码新的数据块
        const newText = decoder.decode(value, { stream: true });

        // 临时隐藏光标
        hideCursor();

        // 只追加新文本，而不是每次都重新渲染整个内容
        robot.appendChunk(newText);

        // 重新显示光标
        showCursor();

        // 确保滚动到底部
        document.documentElement.scrollTo(0, document.documentElement.scrollHeight);
    }

    // 确保响应完成后移除光标
    hideCursor();

    robot.over();
};
