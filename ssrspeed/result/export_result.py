#coding:utf-8

from PIL import Image,ImageDraw,ImageFont
import json
import os
import sys
import time
import logging
logger = logging.getLogger("Sub")

from .upload_result import pushToServer
from .sorter import Sorter
from .exporters import ExporterWps

from config import config

'''
	resultJson
		{
			"group":"GroupName",
			"remarks":"Remarks",
			"loss":0,#Data loss (0-1)
			"ping":0.014,
			"gping":0.011,
			"dspeed":12435646 #Bytes
			"maxDSpeed":12435646 #Bytes
		}
'''

class ExportResult(object):
	def __init__(self):
		self.__config = config["exportResult"]
		self.__hide_max_speed = config["exportResult"]["hide_max_speed"]
		self.__hide_ntt = not config["ntt"]["enabled"]
		self.__hide_netflix = not config["netflix"]
		self.__hide_stspeed = not config["StSpeed"]
		self.__colors = {}
		self.__colorSpeedList = []
		self.__font = ImageFont.truetype(self.__config["font"],18)
		self.__timeUsed = "N/A"
	#	self.setColors()

	def setColors(self,name = "origin"):
		for color in self.__config["colors"]:
			if (color["name"] == name):
				logger.info("Set colors as {}.".format(name))
				self.__colors = color["colors"]
				self.__colorSpeedList.append(0)
				for speed in self.__colors.keys():
					try:
						self.__colorSpeedList.append(float(speed))
					except:
						continue
				self.__colorSpeedList.sort()
				return
		logger.warn("Color {} not found in config.".format(name))

	def setTimeUsed(self, timeUsed):
		self.__timeUsed = time.strftime("%H:%M:%S", time.gmtime(timeUsed))
		logger.info("Time Used : {}".format(self.__timeUsed))

	def export(self,result,split = 0,exportType = 0,sortMethod = ""):
		if (not exportType):
			self.__exportAsJson(result)
		sorter = Sorter()
		result = sorter.sortResult(result,sortMethod)
		self.__exportAsPng(result)

	def exportWpsResult(self, result, exportType = 0):
		if not exportType:
			result = self.__exportAsJson(result)
		epwps = ExporterWps(result)
		epwps.export()

	def __getMaxWidth(self,result):
		font = self.__font
		draw = ImageDraw.Draw(Image.new("RGB",(1,1),(255,255,255)))
		maxGroupWidth = 0
		maxRemarkWidth = 0
		for item in result:
			group = item["group"]
			remark = item["remarks"]
			maxGroupWidth = max(maxGroupWidth,draw.textsize(group,font=font)[0])
			maxRemarkWidth = max(maxRemarkWidth,draw.textsize(remark,font=font)[0])
		return (maxGroupWidth + 10,maxRemarkWidth + 10)
	
	'''
	def __deweighting(self,result):
		_result = []
		for r in result:
			isFound = False
			for i in range(0,len(_result)):
				_r = _result[i]
				if (_r["group"] == r["group"] and _r["remarks"] == r["remarks"]):
					isFound = True
					if (r["dspeed"] > _r["dspeed"]):
						_result[i] = r
					elif(r["ping"] < _r["ping"]):
						_result[i] = r
					break
			if (not isFound):
				_result.append(r)
		return _result
	'''

	def __getBasePos(self, width, text):
		font = self.__font
		draw = ImageDraw.Draw(Image.new("RGB",(1,1),(255,255,255)))
		textSize = draw.textsize(text, font=font)[0]
		basePos = (width - textSize) / 2
		logger.debug("Base Position {}".format(basePos))
		return basePos

	def __exportAsPng(self,result):
		if (self.__colorSpeedList == []):
			self.setColors()
	#	result = self.__deweighting(result)
		resultFont = self.__font
		generatedTime = time.localtime()
		imageHeight = len(result) * 30 + 30 
		weight = self.__getMaxWidth(result)
		groupWidth = weight[0]
		remarkWidth = weight[1]
		if (groupWidth < 60):
			groupWidth = 60
		if (remarkWidth < 60):
			remarkWidth = 90
		otherWidth = 100
	
		groupRightPosition = groupWidth
		remarkRightPosition = groupRightPosition + remarkWidth
		lossRightPosition = remarkRightPosition + otherWidth
		tcpPingRightPosition = lossRightPosition + otherWidth
		googlePingRightPosition = tcpPingRightPosition + otherWidth + 25
		dspeedRightPosition = googlePingRightPosition + otherWidth
		maxDSpeedRightPosition = dspeedRightPosition     
		imageRightPosition = dspeedRightPosition
		ntt_right_position = imageRightPosition
		netflix_right_position = imageRightPosition

		if not self.__hide_max_speed:
			imageRightPosition = maxDSpeedRightPosition + otherWidth 
		maxDSpeedRightPosition = imageRightPosition              

		if not self.__hide_ntt:
			imageRightPosition = imageRightPosition + otherWidth + 80
		ntt_right_position = imageRightPosition
            
		if not self.__hide_netflix:
			imageRightPosition = imageRightPosition + otherWidth + 60
		netflix_right_position = imageRightPosition

		newImageHeight = imageHeight + 30 * 3
		resultImg = Image.new("RGB",(imageRightPosition, newImageHeight),(255,255,255))
		draw = ImageDraw.Draw(resultImg)

		
	#	draw.line((0,newImageHeight - 30 - 1,imageRightPosition,newImageHeight - 30 - 1),fill=(127,127,127),width=1)
		text = "机场奈飞解锁批量检测工具 Mod By 肥羊".format(config["VERSION"])
		draw.text((self.__getBasePos(imageRightPosition, text), 4),
			text,
			font=resultFont,
			fill=(0,0,0)
		)
		draw.line((0, 30, imageRightPosition - 1, 30),fill=(127,127,127),width=1)

		draw.line((1, 0, 1, newImageHeight - 1),fill=(127,127,127),width=1)
		draw.line((groupRightPosition, 30, groupRightPosition, imageHeight + 30 - 1),fill=(127,127,127),width=1)
		draw.line((remarkRightPosition, 30, remarkRightPosition, imageHeight + 30 - 1),fill=(127,127,127),width=1)

		if not self.__hide_netflix:
			draw.line((netflix_right_position, 30, netflix_right_position, imageHeight + 30 - 1),fill=(127,127,127),width=1)  
            
		draw.line((imageRightPosition, 0, imageRightPosition, newImageHeight - 1),fill=(127,127,127),width=1)
	
		draw.line((0,0,imageRightPosition - 1,0),fill=(127,127,127),width=1)

		draw.text(
			(
				self.__getBasePos(groupRightPosition, "Group"), 30 + 4
			),
			"Group", font=resultFont, fill=(0,0,0)
		
		)

		draw.text(
			(
				groupRightPosition + self.__getBasePos(remarkRightPosition - groupRightPosition, "Remarks"), 30 + 4
			),
			"Remarks", font=resultFont, fill=(0,0,0)
		
		)
	
		if not self.__hide_netflix:
			draw.text(
				(
					ntt_right_position + self.__getBasePos(netflix_right_position - ntt_right_position, "Netfilx 解锁"), 30 + 4
					),
				"Netfilx 解锁", font=resultFont, fill=(0,0,0)
			)	
		draw.line((0, 60, imageRightPosition - 1, 60),fill=(127,127,127),width=1)

		totalTraffic = 0
		onlineNode = 0
		for i in range(0,len(result)):
			totalTraffic += result[i]["trafficUsed"] if (result[i]["trafficUsed"] > 0) else 0
			if ((result[i]["ping"] > 0 and result[i]["gPing"] > 0) or (result[i]["dspeed"] > 0)):
				onlineNode += 1
			
			j = i + 1
			draw.line((0,30 * j + 60, imageRightPosition, 30 * j + 60), fill=(127,127,127), width=1)
			item = result[i]

			group = item["group"]
			draw.text((5,30 * j + 30 + 4),group,font=resultFont,fill=(0,0,0))

			remarks = item["remarks"]
			draw.text((groupRightPosition + 5,30 * j + 30 + 4),remarks,font=resultFont,fill=(0,0,0,0))

			if not self.__hide_netflix:
				netflix_type = item["Ntype"]
				pos = ntt_right_position + self.__getBasePos(netflix_right_position - ntt_right_position, netflix_type)
				draw.text((pos, 30 * j + 30 + 1), netflix_type,font=resultFont,fill=(0,0,0))
                    
		files = []
		if (totalTraffic < 0):
			trafficUsed = "N/A"
		else:
			trafficUsed = self.__parseTraffic(totalTraffic)

		draw.text((5, imageHeight + 30 + 4),
			"注：原生解锁和DNS解锁只是解锁方式有区别，在电视端使用时DNS解锁“可能”会提示使用代理，None表示该节点可用，但看不了奈飞，N/A表示该节点不可用  本次节点存活情况: [{}/{}]".format(
				onlineNode,
				len(result)
			),
			font=resultFont,
			fill=(0,0,0)
		)
	#	draw.line((0,newImageHeight - 30 * 3 - 1,imageRightPosition,newImageHeight - 30 * 3 - 1),fill=(127,127,127),width=1)
		draw.text((5,imageHeight + 30 * 2 + 4),
			"肥羊的YouTuBe频道：https://v1.mk/yt  本次更新时间：{}".format(
				time.strftime("%Y-%m-%d %H:%M:%S", generatedTime)
			),
			font=resultFont,
			fill=(0,0,0)
		)
		draw.line((0,newImageHeight - 30 - 1,imageRightPosition,newImageHeight - 30 - 1),fill=(127,127,127),width=1)
		'''
		draw.line((0,newImageHeight - 30 - 1,imageRightPosition,newImageHeight - 30 - 1),fill=(127,127,127),width=1)
		draw.text((5,imageHeight + 30 * 2 + 4),
			"By SSRSpeed {}.".format(
				config["VERSION"]
			),
			font=resultFont,
			fill=(0,0,0)
		)
		'''
		
		draw.line((0,newImageHeight - 1,imageRightPosition,newImageHeight - 1),fill=(127,127,127),width=1)
		filename = "./results/" + time.strftime("%Y-%m-%d-%H-%M-%S", generatedTime) + ".png"
		resultImg.save(filename)
		files.append(filename)
		logger.info("Result image saved as %s" % filename)
		
		for _file in files:
			if (not self.__config["uploadResult"]):
				break
			pushToServer(_file)

	def __parseTraffic(self,traffic):
		traffic = traffic / 1024 / 1024
		if (traffic < 1):
			return("%.2f KB" % (traffic * 1024))
		gbTraffic = traffic / 1024
		if (gbTraffic < 1):
			return("%.2f MB" % traffic)
		return ("%.2f GB" % gbTraffic)

	def __parseSpeed(self,speed):
		speed = speed / 1024 / 1024
		if (speed < 1):
			return("%.2fKB" % (speed * 1024))
		else:
			return("%.2fMB" % speed)

	def __newMixColor(self,lc,rc,rt):
	#	print("RGB1 : {}, RGB2 : {}, RT : {}".format(lc,rc,rt))
		return (
			int(lc[0]*(1-rt)+rc[0]*rt),
			int(lc[1]*(1-rt)+rc[1]*rt),
			int(lc[2]*(1-rt)+rc[2]*rt)
		)

	def __getColor(self,data):
		if (self.__colorSpeedList == []):
			return (255,255,255)
		rt = 1
		curSpeed = self.__colorSpeedList[len(self.__colorSpeedList)-1]
		backSpeed = 0
		if (data >= curSpeed  * 1024 * 1024):
			return (self.__colors[str(curSpeed)][0],self.__colors[str(curSpeed)][1],self.__colors[str(curSpeed)][2])
		for i in range (0,len(self.__colorSpeedList)):
			curSpeed = self.__colorSpeedList[i] * 1024 * 1024
			if (i > 0):
				backSpeed = self.__colorSpeedList[i-1]
			backSpeedStr = str(backSpeed)
		#	print("{} {}".format(data/1024/1024,backSpeed))
			if (data < curSpeed):
				rgb1 = self.__colors[backSpeedStr] if backSpeed > 0 else (255,255,255)
				rgb2 = self.__colors[str(self.__colorSpeedList[i])]
				rt = (data - backSpeed * 1024 * 1024)/(curSpeed - backSpeed * 1024 * 1024)
				logger.debug("Speed : {}, RGB1 : {}, RGB2 : {}, RT : {}".format(data/1024/1024,rgb1,rgb2,rt))
				return self.__newMixColor(rgb1,rgb2,rt)
		return (255,255,255)


	def __exportAsJson(self,result):
		return result

