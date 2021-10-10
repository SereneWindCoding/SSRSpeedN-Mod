# SSRSpeedN-Mod
[机场奈飞解锁批量检测工具](https://github.com/youshandefeiyang/SSRSpeedN-Mod)基于项目[PauperZ/SSRSpeedN](https://github.com/PauperZ/SSRSpeedN)，砍掉测速功能（频繁测速会给机场其他用户造成巨大的影响），仅输出奈飞解锁检测，几乎不消耗任何流量！<br/>
## 效果预览：
![avatar](https://cdn.jsdelivr.net/gh/youshandefeiyang/webcdn@v4.3/share.png)
## 使用方法【仅保证在Windows端正常运行】：
1.安装Python 3.10.0（本项目以提供）！

2.在检测工具根目录打开`开始检测.bat`，首先输入`3`获取管理员权限，然后输入`2`安装好运行所需依赖，安装好依赖后退出，重新打开`开始检测.bat`，输入`1`并按照提示开始检测！

3.如果想要设置7x24H自动检测，需要在Windows Server部署，并增加计划任务和批处理脚本，输出图片可以更改为固定名称，web前端图片属性加随机数即可做到本地浏览器不缓存
```
<img class="no-cache" src="./jiancetu.png" width="100%" height="100%">
<script type="text/javascript">
var suiji = document.getElementsByClassName('no-cache');
for (var i = 0; i < nods.length; i++){
    suiji[i].attributes['src'].value += "?a=" + Math.random();
}
</script>
```

4.不会的可以去看[视频教程](https://www.youtube.com/watch?v=tTv1muckTFg)！
