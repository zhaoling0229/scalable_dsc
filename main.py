import torch
import torch.optim as optim
from torch.utils.data import DataLoader
from mydataset import MyDatset
from res_senet import *
from spectralnet import *
from tqdm import tqdm
from loss import *

def train_se(senet,train_loader,epochs):
	optimizer = optim.Adam(senet.parameters(), lr=0.001)
	scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer)
	for epoch in range(epochs):
		print("epoch:",epoch)
		pbar = tqdm(train_loader)
		for feature,_ in pbar:
			out = senet(feature)
			loss = compute_se_loss(out,feature)
			loss.backward()
			optimizer.step()
			scheduler.step()

def train(config):
	"""
	训练的脚本，待实现的逻辑为：
	1. 传入config配置文件以
	2. 加载数据，采用dataloader或者其他
	3. 数据输入model，得到输出
	4. 根据输出进行聚类，生成伪标签
	5. 计算相似度，选出高的作为正样本，低的作为负样本
	6. 计算损失函数，包括谱聚类损失，伪监督损失以及对比损失
	7. 反向传播，记录损失
	8. 保存模型
	"""
	data_path = config["dataset"]["path"]
	data_num = config["dataset"]["num"]
	batch_size = config["dataset"]["batch_size"]
	data = MyDatset(data_path=data_path)
	train_loader = DataLoader(data, batch_size=batch_size, shuffle=False)

	input_dims, hid_dims, out_dim = config["se_model"]["input_dims"],config["se_model"]["hid_dims"],config["se_model"]["output_dims"]

	senet = mlp(input_dims, hid_dims, out_dim)
	train_se(senet,train_loader,100000)

	model = SpectralNet(config)
	optimizer = optim.Adam(model.parameters(), lr=0.001)
	scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer)
	for epoch in range(10000):
		print("epoch:",epoch)
		pbar = tqdm(train_loader)
		for feature,_ in pbar:
			out = model(feature)
			loss = compute_spec_loss(out,feature)
			loss.backward()
			optimizer.step()
			scheduler.step()
	

def read_config(path):
	"""
	解析配置文件，输入为配置文件路径，输出为字典
	"""
	pass

if __name__ == "__main__":
	"""
	主函数中把所有逻辑串起来
	1. 加载数据 
	2. 实例化model
	3. 加载配置文件
	4. 训练
	5. 评估模型
	6. 记录结果
	"""
	config_path = ""
	config = read_config(config_path)
	
