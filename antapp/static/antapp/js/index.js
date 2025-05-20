var { createUserContent, createRobotContent } = (() => {
    marked.setOptions({
        highlight: function (code, lang) {
            if (lang && hljs.getLanguage(lang)) {
                return hljs.highlight(code, { language: lang }).value;
            }
            return hljs.highlightAuto(code).value;
        }
    });
    const txt = document.querySelector('.send textarea');
    txt.addEventListener('input', () => {
        txt.style.height = 'auto';
        txt.style.height = txt.scrollHeight + 'px';
    });
    const main = document.querySelector('.main');

    function _createUserContent(username, content) {
        const dom = document.createElement('div');
        dom.className = 'user block';
        dom.innerHTML = ` <div class="container">
    <div class="avatar">
    ${username}
    </div>
    <div class="content markdown-body">
    ${_normalizeContent(content)}
    </div>
</div>`;
        const hitBottom = isBottom();
        main.appendChild(dom);
        if (hitBottom) {
            document.documentElement.scrollTo(0, 1000000);
        }
    }

    function _normalizeContent(content) {
        const html = marked.parse(content, {
            breaks: true,
            gfm: true
        });
        return html;
    }
    const textarea = document.querySelector('.send textarea');
    function createUserContent(username) {
        const content = textarea.value.trim();
        _createUserContent(username, content);
        textarea.value = '';
        textarea.style.height = 'auto';
    }
    function _getLastTextNode(dom) {
        const children = dom.childNodes;
        for (let i = children.length - 1; i >= 0; i--) {
            const node = children[i];
            if (node.nodeType === Node.TEXT_NODE && /\S/.test(node.nodeValue)) {
                node.nodeValue = node.nodeValue.replace(/\s+$/, '');
                return node;
            } else if (node.nodeType === Node.ELEMENT_NODE) {
                const last = _getLastTextNode(node);
                if (last) {
                    return last;
                }
            }
        }
        return null;
    }
    function _updateCursor(dom) {
        const contentDom = dom;
        const lastText = _getLastTextNode(contentDom);
        const textNode = document.createTextNode('\u200b');
        if (lastText) {
            lastText.parentElement.appendChild(textNode);
        } else {
            contentDom.appendChild(textNode);
        }
        const domRect = contentDom.getBoundingClientRect();
        const range = document.createRange();
        range.setStart(textNode, 0);
        range.setEnd(textNode, 0);
        const rect = range.getBoundingClientRect();
        const x = rect.left - domRect.left;
        const y = rect.top - domRect.top;
        dom.style.setProperty('--x', `${x}px`);
        dom.style.setProperty('--y', `${y}px`);
        textNode.remove();
    }

    function isBottom() {
        const main = document.querySelector('.main');
        return Math.abs(main.scrollTop + main.clientHeight - main.scrollHeight) < 20;
    }

    function createRobotContent() {
        const dom = document.createElement('div');
        dom.className = 'robot block typing';
        dom.innerHTML = ` <div class="container">
    <div class="avatar">
    <img src="/static/antapp/asset/gpt-avatar.svg" alt="" />
    </div>
    <div class="content markdown-body" style="--x: -1000px; --y: 0px"></div>
  </div>`;

        const contentDom = dom.querySelector('.content');
        let content = '';
        main.appendChild(dom);
        _updateCursor(contentDom);
        const form = document.querySelector('.send');
        form.classList.add('waiting');

        // 为流式输出准备的解析器
        const parser = new DOMParser();
        let lastRenderedLength = 0;

        // 追加整个内容（重新渲染）
        function append(text) {
            content = text;
            const html = _normalizeContent(content);
            const hitBottom = isBottom();

            contentDom.innerHTML = html;
            if (hitBottom) {
                document.documentElement.scrollTo(0, 1000000);
            }
            _updateCursor(contentDom);
        }

        // 增量追加文本（流式渲染）
        function appendChunk(chunk) {
            if (!chunk) return;

            // 更新总内容
            content += chunk;

            // 使用marked解析增量内容
            const newHtml = _normalizeContent(content);

            // 如果是第一次渲染或内容变化很大，直接替换整个内容
            if (lastRenderedLength === 0 || Math.abs(lastRenderedLength - content.length) > 100) {
                contentDom.innerHTML = newHtml;
                lastRenderedLength = content.length;
                return;
            }

            // 否则，尝试智能地只更新新增部分
            try {
                // 解析新的HTML内容
                const newDoc = parser.parseFromString(newHtml, 'text/html');
                const newContentDom = newDoc.body.firstChild;

                // 如果新的内容DOM不存在，则回退到完全替换
                if (!newContentDom) {
                    contentDom.innerHTML = newHtml;
                    lastRenderedLength = content.length;
                    return;
                }

                // 清空现有内容，添加新内容
                contentDom.innerHTML = newHtml;

                // 更新渲染长度
                lastRenderedLength = content.length;

                // 保持滚动位置
                const hitBottom = isBottom();
                if (hitBottom) {
                    document.documentElement.scrollTo(0, 1000000);
                }
            } catch (e) {
                // 如果出错，回退到完全替换
                contentDom.innerHTML = newHtml;
                lastRenderedLength = content.length;
            }

            // 更新光标位置
            _updateCursor(contentDom);
        }

        return {
            append,
            appendChunk,
            over() {
                dom.classList.remove('typing');
                form.classList.remove('waiting');
            },
            getContentDom() {
                return contentDom;
            }
        };
    }
    document.querySelector('.img-btn').onclick = function () {
        document.querySelector('.img-upload').click();
    };

    document.querySelector('.img-upload').onchange = function (e) {
        const preview = document.querySelector('.img-preview');
        const files = e.target.files;

        // 遍历所有选中的文件
        for (let file of files) {
            if (file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    const img = document.createElement('img');
                    img.src = e.target.result;
                    img.style.maxWidth = '200px';
                    img.style.maxHeight = '200px';
                    img.style.margin = '5px';
                    img.style.objectFit = 'cover';
                    preview.appendChild(img);
                };
                reader.readAsDataURL(file);
            }
        }
    };

    return {
        createUserContent,
        createRobotContent,
        isBottom
    };
})();
