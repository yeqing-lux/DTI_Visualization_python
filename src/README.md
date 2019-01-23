### 测试代码

```
python test.py
```



### 测试数据

暂时只使用 gk2-rcc-mask.nii 文件进行过相关测试。



### 文件说明

- test.py为测试文件，可以用来生成纤维

- gui_settings.py为GUI界面、按钮等功能的实现，具体见代码
- util.py的函数介绍：
  - read():读取文件
  - generate_direction_dic():生成将体素与主特征向量、颜色、FA值对应的字典
  - track():对于初始随机种子，计算得到纤维轨迹
  - generate_volume_data()：生成用于体渲染的数据，返回vtkImageData对象
  - createLine():可视化纤维的主要方法
  - ROIsearch():筛选出通过ROI区域的纤维
  - ROI_circlePolyData():生成用于可视化的数据，返回vtkActor对象
  - initial_seed():设置随机种子，并作为track()的自变量用以计算纤维轨迹
  - slice():生成三个视角的切片截面，具体见report







