// 引入express
const express = require('express');

// 创建应用对象
const app = express();

app.all('/submit', (request, response) => {
    response.setHeader('Access-Control-Allow-Origin', '*');
    response.setHeader('Access-Control-Allow-Headers', '*');

    const data = {
        name: '厦门鼓浪屿',
        cloud: 18,
        score: 99,
        open_time: '2021-02-23 16:00:00',
        must_know: 'abababaab',
        introduction_text: '这是一个美丽的地方',
        introduction_audio: 'https://www.baidu.com',
        introduction_vidio: 'https://www.taobao.com',
        msg: '1'
    }
    // 设置响应
    response.send(JSON.stringify(data));
})

// 监听端口启动服务
app.listen(8000, () => {
    console.log('服务已启动，8000端口监听中');
})