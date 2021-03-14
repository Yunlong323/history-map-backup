document.addEventListener('DOMContentLoaded', function () {

    // 侧边tab栏切换
    var tab = document.querySelector('.tab').querySelectorAll('li');
    var right = document.querySelectorAll('.right');
    for (let i = 0; i < tab.length; i++) {
        tab[i].addEventListener('click', function () {
            // 先清除所有效果
            for (var j = 0; j < tab.length; j++) {
                tab[j].className = "";
                right[j].style.display = "none";
            }
            this.className = 'current';
            right[i].style.display = "block";
        })
    }

    // 添加景点信息准备
    var write = document.querySelector('.add').querySelectorAll('.box');
    var name_t = write[0].querySelector('input');
    var xmu_t = write[1].querySelector('input');
    var cloud_t = write[2].querySelector('input');
    var score_t = write[3].querySelector('input');
    var open_time_t = write[4].querySelector('input');
    var must_know_t = write[5].querySelector('textarea');
    var intro_text_t = write[6].querySelector('textarea');
    var intro_audio_t = write[7].querySelector('input');
    var intro_vidio_t = write[8].querySelector('input');
    var btn = document.querySelector('.add').querySelector('.sub');
    var fill = document.querySelectorAll('.fill');
    var icon = document.querySelector('.add').querySelectorAll('i');
    var del = document.querySelector('.table').querySelectorAll('a');
    var last_icon = document.querySelector('.last_icon');
    var radio = document.querySelectorAll('.radio');


    // 向后端请求删除操作
    function cut(number, obj) {
        var nam;
        var flag;
        for (let key in Object.keys(obj)) {
            if (key == number) {
                nam = obj[key].name;
                console.log(nam);
            }
            // console.log(obj[key]);
            // console.log(key);
            // console.log(obj);
        }
        axios({
            method: 'GET',
            url: 'http://https://sishi.xmu.edu.cn/delete_scenery_node',
            params: {
                name: nam
            }
        }).then(response => {
            console.log(response);
            // 判断是否删除成功
            flag = response.data.msg;
            if (flag == '1') {
                alert('删除成功！');
                remove_all(table, ul);
                get_all();
            }
            else {
                alert('删除失败。');
            }
        }, err => {
            console.log(err);
            console.log('执行删除操作请求数据失败。');
        })
    }

    // 未填写报错
    for (let i = 0; i < fill.length; i++) {
        fill[i].addEventListener('blur', function () {
            if (this.value == '') {
                icon[i].innerHTML = '&#xe633;';
                icon[i].style.color = 'red';
            } else {
                icon[i].innerHTML = '&#xe61e;';
                icon[i].style.color = '#13b313';
            }
        })
    }

    // 最后一项单选框点击即正确
    for (let i = 0; i < radio.length; i++) {
        radio[i].addEventListener('click', function () {
            last_icon.innerHTML = '&#xe61e;';
            last_icon.style.color = '#13b313';
        })
    }


    // 后端获取完整景点数据并遍历显示
    function get_all() {
        axios({
            method: 'GET',
            url: 'https://sishi.xmu.edu.cn/display_sceneries'
        }).then(response => {
            // console.log(response);
            // 遍历显示
            for (let i = 0; i < response.data.length; i++) {
                create_ele(response.data[i]);
            }
            // 重新获取del重数
            del = document.querySelector('.table').querySelectorAll('a');
            ul = document.querySelector('.table').querySelectorAll('ul');
            table = document.querySelector('.table');
            console.log(del.length);
            // 在ajax内监听添加的删除事件
            for (let i = 0; i < del.length; i++) {
                // console.log(i);
                del[i].onclick = function () {
                    cut(i, response.data);
                }
            }
            // cut(del.length);
        }, err => {
            console.log(err);
            console.log('获取完整景点信息请求数据失败。');
        })

    }
    // 进入页面直接执行
    get_all();

    // 创建数据列表并显示
    function create_ele(obj) {
        var ul = document.createElement('ul');
        var table = document.querySelector('.table');
        table.appendChild(ul);
        // 遍历赋值
        for (let key of Object.keys(obj)) {
            if (key == 'label_list') {
                for (let i = 0; i < 2; i++) {
                    var li = document.createElement('li');
                    ul.appendChild(li);
                    li.innerHTML = obj[key][i];
                }
            }
            else {
                var li = document.createElement('li');
                ul.appendChild(li);
                li.innerHTML = obj[key];
            }

        }
        // 添加最后一个li
        var li = document.createElement('li');
        var a = document.createElement('a');
        a.href = 'javascript:;';
        a.innerHTML = '删除';
        li.appendChild(a);
        ul.appendChild(li);
    }

    // 清除所有数据列表
    function remove_all(table, ul) {
        for (let i = 1; i < ul.length; i++) {
            table.removeChild(ul[i]);
        }
    }

    // 填写成功后向后端发起请求添加景点数据
    btn.addEventListener('click', function () {
        var selector;
        var flag_last = false;
        for (let i = 0; i < radio.length; i++) {
            if (radio[i].checked == true) {
                selector = i;
                flag_last = true;
            }
        }
        // console.log('被选中的项目是' + selector);
        if (selector == 1) {
            selector = 'unsignable';
        } else {
            selector = 'signable';
        }
        // console.log('被选中的项目是' + selector);

        // 是否可打卡项未填写报错
        if (flag_last == false) {
            last_icon.innerHTML = '&#xe633;';
            last_icon.style.color = 'red';
        } else {
            last_icon.innerHTML = '&#xe61e;';
            last_icon.style.color = '#13b313';
        }

        if (name_t.value && xmu_t.value && cloud_t.value && score_t.value && open_time_t.value && must_know_t.value && intro_text_t.value && intro_audio_t.value && intro_vidio_t.value && flag_last) {
            // console.log('66');
            // console.log(name_t.value, xmu_t.value, cloud_t.value, score_t.value, open_time_t.value, must_know_t.value, intro_text_t.value, intro_audio_t.value, intro_vidio_t.value);
            axios({
                method: 'GET',
                url: 'https://sishi.xmu.edu.cn/post_scenery_info',
                params: {
                    label_list: JSON.stringify([xmu_t.value, selector]),
                    name: name_t.value,
                    cloud: cloud_t.value,
                    score: score_t.value,
                    open_time: open_time_t.value,
                    must_know: must_know_t.value,
                    intro_text: intro_text_t.value,
                    intro_audio: intro_audio_t.value,
                    intro_vidio: intro_vidio_t.value
                }
            }).then(response => {
                // console.log(response.data);
                // console.log(response.data.msg);
                if (response.data.msg == '1') {
                    alert('创建成功!');
                    // 清除所有原先数据
                    var table = document.querySelector('.table');
                    var ul = table.querySelectorAll('ul');
                    remove_all(table, ul);
                    // 重新请求更新页面
                    get_all();
                }
                else {
                    alert('创建失败。');
                }
            }, err => {
                console.log(err);
                console.log('创建新景点请求数据失败。')
            });
        } else {
            alert('请确认所有信息均已填写');
        }
    })
})