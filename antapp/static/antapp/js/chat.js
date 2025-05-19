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
    while (1) {
        const { done, value } = await reader.read();
        if (done) {
            break;
        }
        const txt = decoder.decode(value);
        robot.append(txt);
    }
    robot.over();
};
