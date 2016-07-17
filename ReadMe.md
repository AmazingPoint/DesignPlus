## 关于这个DesignPlus

### 一个基于python的后端服务

#### 依赖 
###### phantomjs
###### Redis

###### pip依赖:
`selenium`
`pyquery`
`flask`
`redis`
    

#### API
`rest.py` flask入口文件

API基于flask，需要安装flask 0.10.0+

API访问地址:[没有appkey限制，请不要恶意攻击](http://api.datastack.cc)

#### 后台服务，数据爬取工作
`mining.py` 执行数据挖掘工作
#### 使用方法
```python mining.py```
(开始抓取数据，效率不高)

```python rest.py```
(运行API服务器)

#### 具体细节
[我的简书博客---快速入门 基于Flask实现Restful风格API](http://www.jianshu.com/p/3b606a14e6b3)
    
[从python开始一个全栈项目 程序员&设计师福利篇](http://www.jianshu.com/p/2d04368cd56b)
