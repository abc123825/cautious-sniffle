# -*- coding:utf-8 -*-
import json
import random
import re
from asyncio import sleep

import yaml
from mirai import FriendMessage, GroupMessage, At, Plain
from mirai import Image, Startup
from mirai.models.events import BotInvitedJoinGroupRequestEvent, NewFriendRequestEvent, MemberJoinRequestEvent, \
    MemberCardChangeEvent, BotMuteEvent, MemberSpecialTitleChangeEvent, BotJoinGroupEvent, \
    MemberJoinEvent, MemberMuteEvent, MemberUnmuteEvent, BotUnmuteEvent, BotLeaveEventKick, MemberLeaveEventKick, \
    MemberLeaveEventQuit

from plugins.setuModerate import setuModerate


def main(bot, config, moderateKey, logger):
    # 读取设置
    global moderateK
    moderateK = moderateKey
    logger.info("读取群管设置")
    with open('config/welcome.yaml', 'r', encoding='utf-8') as f:
        welcome = yaml.load(f.read(), Loader=yaml.FullLoader)
    memberJoinWelcome = welcome.get("memberJoin")
    sendTemp = welcome.get("sendTemp")
    with open('config/autoSettings.yaml', 'r', encoding='utf-8') as f:
        result = yaml.load(f.read(), Loader=yaml.FullLoader)
    global ModerateApiKeys
    ModerateApiKeys = result.get("moderate").get('apiKeys')
    global mainGroup
    mainGroup = int(config.get("mainGroup"))
    global banWords
    banWords = result.get("moderate").get("banWords")
    #读取用户数据
    logger.info("读取用户数据")
    with open('data/userData.yaml', 'r', encoding='utf-8') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    global userdict
    userdict = data
    with open('config/settings.yaml', 'r', encoding='utf-8') as f:
        result1 = yaml.load(f.read(), Loader=yaml.FullLoader)
    friendsAndGroups = result1.get("加群和好友")
    allowFriendstimes = friendsAndGroups.get("allowFriendstimes")
    GroupSensor = friendsAndGroups.get("GroupSensor")
    autoallowFriend = friendsAndGroups.get("autoallowFriend")
    trustDays = friendsAndGroups.get("trustDays")
    fuckinggroup = friendsAndGroups.get("fuckinggroup")
    fuckingnumber = friendsAndGroups.get("fuckingnumber")  # 低于13人退
    qiandaoT = friendsAndGroups.get("signTimes")

    privateGlmReply = result1.get("chatGLM").get("privateGlmReply")
    trustglmReply = result1.get("chatGLM").get("trustglmReply")

    global superUser
    superUser = []
    for i in userdict.keys():
        data = userdict.get(i)
        times = int(str(data.get('sts')))
        if times > trustDays:
            superUser.append(str(i))

    global blackList
    blackList = result.get("banUser")
    global blGroups
    blGroups = result.get("banGroups")
    global superBlGroups
    superBlGroups = result.get("superBlGroups")

    global blackListID
    blackListID = []

    global master
    master = int(config.get('master'))
    botName = config.get("botName")

    moderate = result.get("moderate")

    global threshold
    threshold = moderate.get("threshold")

    global severGroups
    severGroups = moderate.get("groups")
    global banTime
    banTime = moderate.get("banTime")

    #群成员遭到禁言
    @bot.on(MemberMuteEvent)
    async def whenMute(event: MemberMuteEvent):
        try:
            men = int(json.loads(event.json()).get("member").get("id"))
            opn = int(json.loads(event.json()).get("operator").get("id"))
            text = random.choice(welcome.get("muteEvent"))
            await seeeeeee(bot, men, opn, text, int(json.loads(event.json()).get("member").get("group").get("id")))
        except:
            logger.warning("没事，请忽略")

    # 群成员解除禁言
    @bot.on(MemberUnmuteEvent)
    async def whenunMute(event: MemberUnmuteEvent):
        men = event.member.id
        opn = event.operator.id
        text = random.choice(welcome.get("UnMute").get("memberUnmuteMessage"))
        await seeeeeee(bot, men, opn, text, int(json.loads(event.json()).get("member").get("group").get("id")))
        # await bot.send_group_message(int(json.loads(event.json()).get("member").get("group").get("id")), .replace("%被动%",str(event.member.member_name)).replace("%主动%",str(event.operator.member_name)))

    #bot被解除禁言
    @bot.on(BotUnmuteEvent)
    async def botUUUUU(event: BotUnmuteEvent):
        text = random.choice(welcome.get("UnMute").get("botUnmuteMessage"))
        opn = event.operator.id
        men = bot.qq
        await seeeeeee(bot, men, opn, text, event.operator.group.id)

    #成员被踢出
    @bot.on(MemberLeaveEventKick)
    async def memberKikkk(event: MemberLeaveEventKick):
        men = event.member.id
        opn = event.operator.id
        text = random.choice(welcome.get("quitGroup").get("kickMessage"))
        await seeeeeee(bot, men, opn, text, event.member.group.id)

    #成员自动退群
    @bot.on(MemberLeaveEventQuit)
    async def elfLeave(event: MemberLeaveEventQuit):
        men = event.member.id
        opn = 123
        text = random.choice(welcome.get("quitGroup").get("quitMessage"))
        await seeeeeee(bot, men, opn, text, event.member.id)
        #await bot.send_group_message(int(json.loads(event.json()).get("member").get("group").get("id")), .replace("%主动%", str(event.member.member_name)))

    #bot被踢出群聊
    @bot.on(BotLeaveEventKick)
    async def botKICKED(event: BotLeaveEventKick):
        await bot.send_friend_message(master, "bot被踢出群聊\n群号:" + str(event.group.id) + "\n群名:" + str(
            event.group.name) + "\n操作者:" + str(event.operator.member_name) + str(event.operator.id))
        global blackList
        global blGroups
        if event.group.id in blGroups:
            logger.info("已有黑名单群" + str(event.group.id))
        else:
            blGroups.append(event.group.id)

        if event.operator.id in blackList:
            logger.info("已有黑名单用户" + str(event.operator.id))
        else:
            blackList.append(event.operator.id)

        with open('config/autoSettings.yaml', 'r', encoding='utf-8') as f:
            result = yaml.load(f.read(), Loader=yaml.FullLoader)
        result["banUser"] = blackList
        result["banGroups"] = blGroups
        with open('config/autoSettings.yaml', 'w', encoding="utf-8") as file:
            yaml.dump(result, file, allow_unicode=True)

    #处理加群邀请
    @bot.on(BotInvitedJoinGroupRequestEvent)
    async def checkAllowGroup(event: BotInvitedJoinGroupRequestEvent):
        global superBlGroups
        logger.info("接收来自 " + str(event.from_id) + " 的加群邀请")
        if GroupSensor:
            with open('config/autoSettings.yaml', 'r', encoding='utf-8') as f:
                result23 = yaml.load(f.read(), Loader=yaml.FullLoader)
            youquan = result23.get("trustGroups")

            if event.group_id in superBlGroups:
                await bot.send_friend_message(event.from_id, "该群在禁止名单中！")
                return
            if event.group_id in youquan or event.sender.id == master:
                logger.info("同意")
                al = '同意'
                sdf = "请先向目标群群员确认是否愿意接受bot加群"
                await bot.send_friend_message(event.from_id, sdf)
                await bot.send_friend_message(event.from_id, "40秒后自动同意")
                await sleep(40)
                await bot.allow(event)
            else:
                logger.info("拒绝")
                al = "拒绝"
                await bot.send_friend_message(event.from_id, "该群无授权，请在bot用户群：" + str(
                    mainGroup) + "\n联系机器人管理员获取授权")
        else:
            if str(event.from_id) in userdict.keys():
                try:
                    if int(userdict.get(str(event.from_id)).get("sts")) > qiandaoT or event.sender.id == master:
                        if event.group_id in superBlGroups:
                            await bot.send_friend_message(event.from_id, "该群已被禁止")
                            return
                        if event.group_id in blGroups:
                            await bot.send_friend_message(event.from_id,
                                                          "该群在黑名单内.\n解除拉黑请前往本bot用户群" + str(
                                                              mainGroup) + "在群内发送\n/blgroup remove 群号")
                            return
                        logger.info("同意")
                        al = '同意'
                        sdf = "请先向目标群群员确认是否愿意接受bot加群"
                        await bot.send_friend_message(event.from_id, sdf)
                        await bot.send_friend_message(event.from_id, "40秒后自动同意")
                        await sleep(40)
                        await bot.allow(event)
                    else:
                        logger.info("签到天数不够，拒绝")
                        al = '拒绝'
                        await bot.send_friend_message(event.from_id, "群内签到天数不够呢，需要的签到天数" + str(
                            qiandaoT) + "。\n也可前往用户群" + str(
                            mainGroup) + " 获取授权\n在该群内发送:\n授权#你的QQ")
                except:
                    pass
            else:
                logger.info("非用户，拒绝")
                al = '拒绝'
                await bot.send_friend_message(event.from_id, "无用户签到记录，请在任意bot共同群聊内发送 签到 达到" + str(
                    qiandaoT) + "天以上\n也可前往用户群" + str(
                    mainGroup) + " 获取授权\n在该群内发送:\n授权#你的QQ")
        await bot.send_friend_message(master, '有新的加群申请\n来自：' + str(event.from_id) + '\n目标群：' + str(
            event.group_id) + '\n昵称：' + event.nick + '\n状态：' + al)

    #新人入群欢迎
    @bot.on(MemberJoinEvent)
    async def MemberJoinHelper(event: MemberJoinEvent):
        if random.choice(memberJoinWelcome) == 1:
            return
        if event.member.group.id == 623265372:
            await bot.send_group_message(event.member.group.id, [At(event.member.id),
                                                                 "\n提问前请翻阅：\n常见问题汇总：https://docs.qq.com/aio/DTXNRVnZYYm5TQWhM\n项目wiki:https://github.com/avilliai/Manyana/wiki\n项目文档：https://github.com/avilliai/Manyana\n\n提问附上控制台截图。"])
            return
        await bot.send_group_message(event.member.group.id, (
        At(event.member.id), random.choice(memberJoinWelcome).replace("botName", botName).replace(r"\n", "\n")))

    #bot加群
    @bot.on(BotJoinGroupEvent)
    async def botJoin(event: BotJoinGroupEvent):

        await bot.send_group_message(event.group.id, "已加入服务群聊....")
        if fuckinggroup:
            gid = event.group.id

            with open('config/autoSettings.yaml', 'r', encoding='utf-8') as f:
                result23 = yaml.load(f.read(), Loader=yaml.FullLoader)
            youquan1 = result23.get("trustGroups")

            try:
                sf = await bot.member_list(int(gid))
                sf = len(sf.data)
            except Exception as e:
                logger.error(e)
                return
            try:
                if sf < fuckingnumber and gid not in youquan1:
                    await bot.send_group_message(gid, "无授权小群，自动退出。")
                    logger.warning("已清退:" + str(gid))
                    await bot.quit(gid)
                    return
            except Exception as e:
                logger.error(e)
        await bot.send_group_message(event.group.id, "发送 @" + str(
            botName) + " 帮助 以获取功能列表\n项目地址：https://github.com/avilliai/Manyana\n喜欢bot的话可以给个star哦(≧∇≦)ﾉ")

    #自动更新数据
    @bot.on(Startup)
    async def updateData(event: Startup):
        while True:
            await sleep(60)
            # 读取用户数据
            logger.info("更新数据")
            global moderateK
            moderateK = moderateKey
            #logger.info("读取群管设置")
            with open('config/autoSettings.yaml', 'r', encoding='utf-8') as f:
                result = yaml.load(f.read(), Loader=yaml.FullLoader)

            global ModerateApiKeys
            ModerateApiKeys = result.get("moderate").get('apiKeys')
            global mainGroup
            mainGroup = int(config.get("mainGroup"))
            global banWords
            banWords = result.get("moderate").get("banWords")
            # 读取用户数据
            #logger.info("读取用户数据")
            with open('data/userData.yaml', 'r', encoding='utf-8') as file:
                data = yaml.load(file, Loader=yaml.FullLoader)
            global userdict
            userdict = data
            with open('config/settings.yaml', 'r', encoding='utf-8') as f:
                result1 = yaml.load(f.read(), Loader=yaml.FullLoader)

            global superUser
            superUser = []
            for i in userdict.keys():
                data = userdict.get(i)
                times = int(str(data.get('sts')))
                if times > trustDays:
                    superUser.append(str(i))

            global blackList
            blackList = result.get("banUser")
            global blGroups
            blGroups = result.get("banGroups")

            global blackListID
            blackListID = []

            global master
            master = int(config.get('master'))

            moderate = result.get("moderate")

            global threshold
            threshold = moderate.get("threshold")

            global severGroups
            severGroups = moderate.get("groups")

    #处理好友申请
    @bot.on(NewFriendRequestEvent)
    async def allowStranger(event: NewFriendRequestEvent):
        global userdict
        logger.info("新的好友申请，来自" + str(event.from_id))
        if (str(event.from_id) in userdict.keys() and int(
                userdict.get(str(event.from_id)).get("sts")) > allowFriendstimes) or autoallowFriend:
            logger.info("有用户记录，同意")
            al = '同意'
            await bot.allow(event)
            await sleep(5)
            await bot.send_friend_message(event.from_id,
                                          "你好ヾ(≧▽≦*)o，bot项目地址：https://github.com/avilliai/Manyana\n觉得还不错的话可以点个star哦")
            await bot.send_friend_message(event.from_id, "群内发送 @" + str(botName) + " 帮助 获取功能列表")
            await bot.send_friend_message(event.from_id, "本bot用户群" + str(mainGroup))
            if not privateGlmReply and trustglmReply:
                await bot.send_friend_message(event.from_id,
                                              "在任意群内累计发送 签到 " + str(trustDays) + "天后将为您开放私聊ai权限")
        else:
            logger.info("无用户记录，拒绝")
            al = '拒绝'
        await bot.send_friend_message(master, '有新的好友申请\n来自：' + str(event.from_id) + '\n来自群：' + str(
            event.group_id) + '\n昵称：' + event.nick + '\n状态：' + al)

    #处理新成员加群申请
    @bot.on(MemberJoinRequestEvent)
    async def allowStrangerInvite(event: MemberJoinRequestEvent):
        logger.info("有新群员加群申请")
        if event.from_id in blackList:
            await bot.send_group_message(event.group_id, "有新的入群请求，存在bot黑名单记录")
        else:
            await bot.send_group_message(event.group_id, '有新的入群请求.....管理员快去看看吧\nQQ：' + str(
                event.from_id) + '\n昵称：' + event.nick + '\n' + event.message)

    #群员称号改变
    @bot.on(MemberSpecialTitleChangeEvent)
    async def honorChange(event: MemberSpecialTitleChangeEvent):
        logger.info("群员称号改变")
        await bot.send_group_message(event.member.group.id,
                                     str(event.member.member_name) + '获得了称号：' + str(event.current))

    #群员昵称改变
    @bot.on(MemberCardChangeEvent)
    async def nameChange(event: MemberCardChangeEvent):
        if len(event.current) > 0:
            logger.info("群员昵称改变")
            if event.origin == "" or event.origin is None:
                return
            else:
                await bot.send_group_message(event.member.group.id,
                                             event.origin + ' 的昵称改成了 ' + event.current + ' \n警惕新型皮套诈骗')

    @bot.on(BotMuteEvent)
    async def BanAndBlackList(event: BotMuteEvent):
        logger.info("bot被禁言，操作者" + str(event.operator.id))
        global blackList
        global blGroups
        if event.operator.group.id in blGroups:
            logger.info("已有黑名单群" + str(event.operator.group.id))
        else:
            if event.operator.group.id != mainGroup:
                blGroups.append(event.operator.group.id)
            else:
                return
        if event.operator.id in blackList:
            logger.info("已有黑名单用户" + str(event.operator.id))
        else:
            blackList.append(event.operator.id)

        with open('config/autoSettings.yaml', 'r', encoding='utf-8') as f:
            result = yaml.load(f.read(), Loader=yaml.FullLoader)
        result["banUser"] = blackList
        result["banGroups"] = blGroups
        with open('config/autoSettings.yaml', 'w', encoding="utf-8") as file:
            yaml.dump(result, file, allow_unicode=True)
        await bot.send_friend_message(master, 'bot在群:\n' + str(event.operator.group.name) + str(
            event.operator.group.id) + '\n被禁言' + str(event.duration_seconds) + '秒\n操作者id：' + str(
            event.operator.id) + '\nname:(' + str(event.operator.member_name) + ')\n已退群并增加不良记录')
        await bot.send_friend_message(master,
                                      "可使用\n/sbg add 群号\n以永久拉黑此群\n/sbg remove 群号\n则为移除该群黑名单")
        await bot.quit(event.operator.group.id)
        logger.info("已退出群 " + str(event.operator.group.id) + " 并拉黑")

    @bot.on(FriendMessage)
    async def quiteG(event: FriendMessage):
        if str(event.message_chain).startswith("退群#") and str(event.sender.id) == str(master):
            dataG = str(event.message_chain).split("#")[1]
            try:
                await bot.quit(int(dataG))
                logger.info("退出：" + str(dataG))
                await bot.send_friend_message(int(master), "已退出: " + str(dataG))
            except:
                logger.warning("不正确的群号")
        if event.sender.id == master:
            global superBlGroups
            if str(event.message_chain).startswith("/sbg "):
                if str(event.message_chain).startswith("/sbg add "):
                    groupId = int(str(event.message_chain).split(" ")[-1])
                    if groupId in superBlGroups:
                        await bot.send(event, f"已存在永久黑名单群{groupId}")
                        return
                    superBlGroups.append(groupId)
                    await bot.send(event, f"成功添加永久黑名单群{groupId}")
                if str(event.message_chain).startswith("/sbg remove "):
                    groupId = int(str(event.message_chain).split(" ")[-1])
                    if groupId not in superBlGroups:
                        await bot.send(event, f"不存在永久黑名单群{groupId}")
                        return
                    superBlGroups.remove(groupId)
                    await bot.send(event, f"成功移除永久黑名单群{groupId}")
                with open('config/autoSettings.yaml', 'r', encoding='utf-8') as f:
                    result = yaml.load(f.read(), Loader=yaml.FullLoader)
                logger.info("当前黑名单" + str(blackList))
                result["superBlGroups"] = superBlGroups
                with open('config/autoSettings.yaml', 'w', encoding="utf-8") as file:
                    yaml.dump(result, file, allow_unicode=True)

    @bot.on(GroupMessage)
    async def help(event: GroupMessage):
        global banWords
        if str(event.group.id) in banWords.keys() and event.sender.id != master:
            group = str(event.sender.group.id)
            try:
                banw = banWords.get(group)

                for i in banw:
                    if i in str(event.message_chain) and i != "":
                        id = event.message_chain.message_id
                        logger.info("获取到违禁词列表" + str(banw))
                        try:
                            await bot.recall(id)
                            logger.info("撤回违禁消息" + str(event.message_chain))
                            await bot.send(event, "检测到违禁词" + i + "，撤回")
                        except:
                            logger.error("关键词撤回失败！")
                        try:
                            await bot.mute(target=event.sender.group.id, member_id=event.sender.id, time=banTime)
                            await bot.send(event, "检测到违禁词" + i + "，禁言")
                        except:
                            logger.error("禁言失败，权限可能过低")

            except:
                pass

    @bot.on(GroupMessage)
    async def checkBanWords(event: GroupMessage):
        global banWords
        if At(bot.qq) in event.message_chain and "违禁词" in str(event.message_chain) and "查" in str(
                event.message_chain):
            group = str(event.sender.group.id)
            banw = str(banWords.get(group)).replace(",", ",\n")
            await bot.send(event, "本群违禁词列表如下：\n" + banw)

    @bot.on(GroupMessage)
    async def addBanWord(event: GroupMessage):
        global banWords
        if (str(event.sender.permission) != "Permission.Member" or str(event.sender.id) == str(
                master)) and "添加违禁词" in str(event.message_chain):
            msg = "".join(map(str, event.message_chain[Plain]))
            # 匹配指令
            m = re.match(r'^添加违禁词\s*(.*)\s*$', msg.strip())
            if m:
                aimWord = m.group(1)
                if str(event.sender.group.id) in banWords:
                    banw = banWords.get(str(event.sender.group.id))
                    banw.append(aimWord)
                    banWords[str(event.sender.group.id)] = banw
                else:
                    banWords[str(event.sender.group.id)] = [aimWord]
                with open('config/autoSettings.yaml', 'r', encoding='utf-8') as f:
                    result = yaml.load(f.read(), Loader=yaml.FullLoader)
                moderate = result.get("moderate")

                moderate["banWords"] = banWords
                result["moderate"] = moderate
                with open('config/autoSettings.yaml', 'w', encoding="utf-8") as file:
                    yaml.dump(result, file, allow_unicode=True)
                await bot.send(event, "已添加违禁词：" + aimWord)

    @bot.on(GroupMessage)
    async def removeBanWord(event: GroupMessage):
        global banWords
        if (str(event.sender.permission) != "Permission.Member" or str(event.sender.id) == str(
                master)) and "删除违禁词" in str(event.message_chain):
            msg = "".join(map(str, event.message_chain[Plain]))
            # 匹配指令
            m = re.match(r'^删除违禁词\s*(.*)\s*$', msg.strip())
            if m:
                aimWord = m.group(1)
                try:
                    newData = banWords.get(str(event.sender.group.id)).remove(aimWord)
                    banWords[str(event.sender.group.id)] == newData
                    with open('config/autoSettings.yaml', 'r', encoding='utf-8') as f:
                        result = yaml.load(f.read(), Loader=yaml.FullLoader)
                    moderate = result.get("moderate")
                    moderate["banWords"] = banWords
                    result["moderate"] = moderate
                    with open('config/autoSettings.yaml', 'w', encoding="utf-8") as file:
                        yaml.dump(result, file, allow_unicode=True)

                    await bot.send(event, "已移除违禁词：" + aimWord)
                except:
                    await bot.send(event, "没有已添加的违禁词：" + aimWord)

    @bot.on(GroupMessage)
    async def geturla(event: GroupMessage):
        global severGroups
        if str(event.group.id) in ModerateApiKeys:
            if (str(event.group.permission) != str('Permission.Member')) and event.message_chain.count(Image) and str(
                    event.group.id) in severGroups:
                lst_img = event.message_chain.get(Image)
                try:
                    moderateK = ModerateApiKeys.get(str(event.group.id))
                except:
                    logger.warning(str(event.group.id) + " 开启色图审核失败，未配置apiKey或apiKey已失效")
                    await bot.send(event, "调用失败，公共apiKey已耗尽本月使用限额或本群配置apiKey已失效")
                    await bot.send(event,
                                   "请在https://www.moderatecontent.com/注册并获取apiKey(不要用QQ邮箱)\n随后群内发送如下指令\n设置审核密钥[apiKey]\n以开启本群审核功能\n例如\n设置审核密钥207b10178c64089dvzv90ebfcd7f865d97a")
                    return
                for i in lst_img:
                    url = i.url
                    logger.info("图片审核:url:" + url + " key:" + moderateK)
                    try:
                        rate = await setuModerate(url, moderateK)
                    except:
                        logger.error(
                            "涩图审核失败，可能是图片太大，也可能是(小概率)api-key达到本月调用次数限制，尝试注册新账号更新新的api-key以解决")
                        return
                    logger.info("图片审核:结果:" + str(rate))
                    threshold = severGroups.get(str(event.group.id))
                    if int(rate) > threshold:
                        await bot.send(event, "检测到图片违规\npredictions-adult:" + str(rate))
                        try:
                            await bot.recall(event.message_chain.message_id)
                        except:
                            logger.error("撤回图片失败")
                        try:
                            await bot.mute(target=event.sender.group.id, member_id=event.sender.id, time=banTime)
                        except:
                            logger.error("禁言失败，权限可能过低")
                        return

    @bot.on(GroupMessage)
    async def geturla(event: GroupMessage):
        global severGroups
        if event.message_chain.count(Image) == 1 and "ping" in str(event.message_chain):
            lst_img = event.message_chain.get(Image)
            url = lst_img[0].url
            logger.info("图片审核:url:" + url)

            try:
                rate = await setuModerate(url, moderateK)
            except:
                logger.error(
                    "涩图审核失败，可能是图片太大，也可能是(小概率)api-key达到本月调用次数限制，尝试注册新账号更新新的api-key以解决")
                await bot.send(event,
                               "涩图审核失败，可能是图片太大，也可能是公共api-key达到本月调用次数限制，尝试为本群配置单独的api-key以解决")
                await bot.send(event,
                               "1、请在https://www.moderatecontent.com/注册并获取apiKey(不要用QQ邮箱)\n2、随后群内发送\n设置审核密钥[apiKey]\n以开启本群审核功能\n3、例如\n设置审核密钥207b10178c64089dvzv90ebfcd7f865d97a")

                return
            logger.info("图片审核:结果:" + str(rate))
            await bot.send(event, "图片检测结果：\npredictions-adult:" + str(rate))

    @bot.on(GroupMessage)
    async def addKeys(event: GroupMessage):
        global severGroups
        global ModerateApiKeys
        if "设置审核密钥" in str(event.message_chain):
            a = str(event.message_chain).split("设置审核密钥")[1]
            if event.sender.id == int(master):
                a = moderateK

            logger.info("测试密钥:" + a)

            try:
                url = 'https://www.moderatecontent.com/img/sample_anime_2.jpg'
                logger.info("图片审核:url:" + url + " key:" + moderateK)
                rate = await setuModerate(url, a)
            except:
                logger.error("无效的apiKey或图片太大")
                await bot.send(event,
                               "涩图审核失败，可能是图片太大，也可能是api-key无效\n尝试注册新账号https://www.moderatecontent.com/获取新的api-key以解决\n指令：设置审核密钥[apiKey]\n示例如下：\n设置审核密钥2f4tga2tarafa4hjohljghvbngnf58")
                return
            logger.info("图片审核:结果:" + str(rate))
            ModerateApiKeys[str(event.group.id)] = a
            with open('config/autoSettings.yaml', 'r', encoding='utf-8') as f:
                result = yaml.load(f.read(), Loader=yaml.FullLoader)
            result["moderate"]["apiKeys"] = ModerateApiKeys
            with open('config/autoSettings.yaml', 'w', encoding="utf-8") as file:
                yaml.dump(result, file, allow_unicode=True)
            await bot.send(event, "设置apiKey成功")

    @bot.on(GroupMessage)
    async def setConfiga(event: GroupMessage):
        global threshold
        global severGroups
        if 1 == 1:
            if str(event.message_chain).startswith("/阈值") and (
                    str(event.sender.permission) != "Permission.Member" or event.sender.id == master):
                if str(event.group.id) in ModerateApiKeys:
                    temp = int(str(event.message_chain)[3:])
                    if temp > 100 or temp < 0:
                        await bot.send(event, "设置阈值不合法")
                    else:
                        try:
                            threshold = temp
                            severGroups[str(event.group.id)] = temp
                            with open('config/autoSettings.yaml', 'r', encoding='utf-8') as f:
                                result = yaml.load(f.read(), Loader=yaml.FullLoader)
                            moderate = result.get("moderate")
                            moderate["groups"] = severGroups
                            result["moderate"] = moderate
                            with open('config/autoSettings.yaml', 'w', encoding="utf-8") as file:
                                yaml.dump(result, file, allow_unicode=True)

                            await bot.send(event, "成功修改撤回阈值为" + str(temp))
                        except:
                            await bot.send(event, "阈值设置出错，请进入config.json中手动设置threshold值")
                else:
                    logger.warning(str(event.group.id) + " 开启色图审核失败，未配置apiKey")
                    await bot.send(event, "公共apiKey达到每月调用次数限制，本群未配置apiKey,无法开启此功能")
                    await bot.send(event,
                                   "1、请在https://www.moderatecontent.com/注册并获取apiKey(不要用QQ邮箱)\n2、随后群内发送\n设置审核密钥[apiKey]\n以开启本群审核功能\n3、例如\n设置审核密钥207b10178c64089dvzv90ebfcd7f865d97a")

        if (str(event.sender.permission) != "Permission.Member" or event.sender.id == master) and str(
                event.message_chain) == "/moderate":
            if str(event.group.id) in ModerateApiKeys:
                if str(event.group.id) in severGroups:
                    logger.info("群:" + str(event.group.id) + " 关闭了审核")
                    severGroups.pop(str(event.group.id))
                    await bot.send(event, "关闭审核")
                else:
                    logger.info("群:" + str(event.group.id) + " 开启了审核")
                    severGroups[str(event.group.id)] = 40
                    await bot.send(event, "开启审核")
                with open('config/autoSettings.yaml', 'r', encoding='utf-8') as f:
                    result = yaml.load(f.read(), Loader=yaml.FullLoader)
                moderate = result.get("moderate")
                moderate["groups"] = severGroups
                result["moderate"] = moderate
                with open('config/autoSettings.yaml', 'w', encoding="utf-8") as file:
                    yaml.dump(result, file, allow_unicode=True)
                await bot.send(event, "ok")
            else:
                logger.warning(str(event.group.id) + " 开启色图审核失败，未配置apiKey")
                await bot.send(event, "公共apiKey达到每月调用次数限制")
                await bot.send(event, "开启色图审核失败，未配置本群apiKey")
                await bot.send(event,
                               "1、请在https://www.moderatecontent.com/注册并获取apiKey(不要用QQ邮箱)\n2、随后群内发送\n设置审核密钥[apiKey]\n以开启本群审核功能\n3、例如\n设置审核密钥207b10178c64089dvzv90ebfcd7f865d97a")

    @bot.on(GroupMessage)
    async def exitBadGroup(event: GroupMessage):
        ls = ["你妈", "傻逼", "死你", "垃圾", "nm", "狗东西", "废物", "低能", "沙比", "啥比", "沙壁", "啥必", "辣鸡",
              "腊鸡", "妈", "爸", "爹", "智障", "死", "逼"]
        if At(bot.qq) in event.message_chain:
            for i in ls:
                if i in str(event.message_chain):
                    logger.warn("敏感词触发者：" + str(event.sender.id))
                    await bot.send_friend_message(master,
                                                  "用户：" + str(event.sender.id) + " 发送了含敏感字消息\n群号：" + str(
                                                      event.group.id) + "\n内容：" + str(
                                                      event.message_chain) + "\n可使用 退群#群号 操作bot退出该群\n或使用\n  /bl add qq号  拉黑指定用户")
                    global blackList
                    global blGroups
                    if event.group.id in blGroups or event.group.id == int(mainGroup):
                        logger.info("不再添加黑名单群：" + str(event.sender.group))
                    else:
                        blGroups.append(event.group.id)

                    if event.sender.id in blackList:
                        logger.info("已有黑名单用户" + str(event.sender.id))
                    else:
                        blackList.append(event.sender.id)

                    with open('config/autoSettings.yaml', 'r', encoding='utf-8') as f:
                        result = yaml.load(f.read(), Loader=yaml.FullLoader)
                    result["banUser"] = blackList
                    result["banGroups"] = blGroups
                    with open('config/autoSettings.yaml', 'w', encoding="utf-8") as file:
                        yaml.dump(result, file, allow_unicode=True)
                    return

    @bot.on(GroupMessage)
    async def AddRemoveBl(event: GroupMessage):
        global superUser, blackList, superBlGroups
        if event.group.id in superBlGroups:
            await bot.send(event, "本群在黑名单内")
            await bot.quit(event.group.id)
            logger.warning(f"已清退永久黑名单群{event.group.id}")
        if event.sender.id == master:
            if str(event.message_chain).startswith("/sbg "):
                if str(event.message_chain).startswith("/sbg add "):
                    groupId = int(str(event.message_chain).split(" ")[-1])
                    if groupId in superBlGroups:
                        await bot.send(event, f"已存在永久黑名单群{groupId}")
                        return
                    superBlGroups.append(groupId)
                    await bot.send(event, f"成功添加永久黑名单群{groupId}")
                if str(event.message_chain).startswith("/sbg remove "):
                    groupId = int(str(event.message_chain).split(" ")[-1])
                    if groupId not in superBlGroups:
                        await bot.send(event, f"不存在永久黑名单群{groupId}")
                        return
                    superBlGroups.remove(groupId)
                    await bot.send(event, f"成功移除永久黑名单群{groupId}")
                with open('config/autoSettings.yaml', 'r', encoding='utf-8') as f:
                    result = yaml.load(f.read(), Loader=yaml.FullLoader)
                logger.info("当前黑名单" + str(blackList))
                result["superBlGroups"] = superBlGroups
                with open('config/autoSettings.yaml', 'w', encoding="utf-8") as file:
                    yaml.dump(result, file, allow_unicode=True)

    @bot.on(GroupMessage)
    async def quitgrrrr(event: GroupMessage):
        if event.sender.id == master and (
                str(event.message_chain).startswith("/quit<") or str(event.message_chain).startswith("/quit＜")):
            try:
                setg = int(str(event.message_chain).replace("/quit<", "").replace("/quit＜", ""))
            except:
                await bot.send(event, "不合法的取值")
                return
            await bot.send(event, "退出所有人数小于" + str(setg) + "的群....")
            asf = await bot.group_list()
            #print(len(asf.data), asf.data)
            with open('config/autoSettings.yaml', 'r', encoding='utf-8') as f:
                result23 = yaml.load(f.read(), Loader=yaml.FullLoader)
            youquan1 = result23.get("trustGroups")
            totalquit = 0
            for nb in asf:
                gid = nb.id
                try:
                    sf = await bot.member_list(int(gid))
                    sf = len(sf.data)
                except Exception as e:
                    logger.error(e)
                    continue
                try:
                    if sf < setg and gid not in youquan1:
                        await bot.send_group_message(gid, "无授权小群，自动退出。")
                        logger.warning("已清退" + str(gid))
                        await bot.quit(gid)
                        totalquit += 1
                except Exception as e:
                    logger.error(e)
                    continue
                    totalquit += 1
            await bot.send(event, "已退出" + str(totalquit) + "个群")

    @bot.on(GroupMessage)
    async def quitgrrrrr(event: GroupMessage):
        if fuckinggroup:
            gid = event.group.id
            if gid==int(mainGroup):
                return
            with open('config/autoSettings.yaml', 'r', encoding='utf-8') as f:
                result23 = yaml.load(f.read(), Loader=yaml.FullLoader)
            youquan1 = result23.get("trustGroups")
            try:
                sf = await bot.member_list(int(gid))
                sf = len(sf.data)
            except Exception as e:
                logger.error(e)
                return
            try:
                if sf < fuckingnumber and gid not in youquan1:
                    await bot.send_group_message(gid, "无授权群，自动退出。")
                    logger.warning("已清退:" + str(gid))
                    await bot.quit(gid)
            except Exception as e:
                logger.error(e)

    @bot.on(GroupMessage)
    async def removeBl(event: GroupMessage):
        if event.sender.id == master or event.sender.id in superUser or event.group.id == mainGroup:
            global blackList
            global blGroups, superBlGroups
            if str(event.message_chain).startswith("/blgroup remove ") or str(event.message_chain).startswith(
                    "移除黑名单群 "):
                try:
                    groupId = int(str(event.message_chain).split(" ")[-1])
                    if groupId in superBlGroups:
                        await bot.send(event, "无法解除群黑名单，拉黑等级过高")
                        return
                    blGroups.remove(groupId)
                    logger.info("成功移除黑名单群" + str(groupId))
                    await bot.send(event, "成功移除黑名单群" + str(groupId))
                    logger.info("当前黑名单群" + str(blGroups))

                    with open('config/autoSettings.yaml', 'r', encoding='utf-8') as f:
                        result11 = yaml.load(f.read(), Loader=yaml.FullLoader)
                    result11["banGroups"] = blGroups
                    with open('config/autoSettings.yaml', 'w', encoding="utf-8") as file:
                        yaml.dump(result11, file, allow_unicode=True)
                    return
                except:
                    logger.error("移除失败，该群不在黑名单中")
                    await bot.send(event, "移除失败，该群不在黑名单中")
            if str(event.message_chain).startswith("/bl remove ") or str(event.message_chain).startswith(
                    " 移除黑名单用户"):
                try:
                    groupId = int(str(event.message_chain).split(" ")[-1])
                    blackList.remove(groupId)
                    logger.info("成功移除黑名单用户" + str(groupId))
                    await bot.send(event, "成功移除黑名单用户" + str(groupId))
                    with open('config/autoSettings.yaml', 'r', encoding='utf-8') as f:
                        result = yaml.load(f.read(), Loader=yaml.FullLoader)
                    result["banUser"] = blackList
                    with open('config/autoSettings.yaml', 'w', encoding="utf-8") as file:
                        yaml.dump(result, file, allow_unicode=True)
                    return
                except:
                    logger.error("移除失败，该用户不在黑名单中")
                    await bot.send(event, "移除失败，该用户不在黑名单中")

    async def seeeeeee(bot, men, opn, text, groupid):
        ta = text.split("%")
        #print(ta)
        while "" in ta:
            ta.remove("")
        #print(ta)
        p = 0
        for i in ta:
            if i == "主动":
                ta[p] = At(opn)
            elif i == "被动":
                ta[p] = At(men)
            else:
                if i == "":
                    ta.remove("")
            p += 1
        #print(ta)
        try:
            await bot.send_group_message(groupid, ta)
        except:
            logger.error("群事件监听出错，不影响运行，请忽略")

    @bot.on(FriendMessage)
    async def getGroupList(event: FriendMessage):
        if event.sender.id == master and (
                str(event.message_chain) == "群列表"):
            r = "群列表如下："
            asf = await bot.group_list()
            # print(len(asf.data), asf.data)
            with open('config/autoSettings.yaml', 'r', encoding='utf-8') as f:
                result23 = yaml.load(f.read(), Loader=yaml.FullLoader)
            youquan1 = result23.get("trustGroups")
            logger.info("获取群列表")
            total = 0
            for nb in asf:
                gid = nb.id
                try:
                    sf = await bot.member_list(int(gid))
                    gname = sf.data[0].group.name
                    if gid in youquan1:
                        logger.info(f"信任群聊：群 {gid} ({gname})\n人数 {len(sf.data)}")
                        r += "\n" + f"信任群聊：群 {gid} ({gname})\n人数 {len(sf.data)}"
                    else:
                        logger.info(f"群 {gid} ({gname})\n人数 {len(sf.data)}")
                        r += "\n" + f"群 {gid} ({gname})\n人数 {len(sf.data)}"
                    total += 1
                except Exception as e:
                    logger.error(e)
                    continue
            await bot.send(event,
                           f"当前群列表：{r}\n总数：{total}\n\n可发送如下指令以退出群聊：\n/quit<7    此指令用于退出所有人数小于7的群聊，数字可更改\n退群#群号     此指令退出指定群聊")

    @bot.on(FriendMessage)
    async def quitgrrrr(event: FriendMessage):
        if event.sender.id == master and (
                str(event.message_chain).startswith("/quit<") or str(event.message_chain).startswith("/quit＜")):
            try:
                setg = int(str(event.message_chain).replace("/quit<", "").replace("/quit＜", ""))
            except:
                await bot.send(event, "不合法的取值")
                return
            await bot.send(event, "退出所有人数小于" + str(setg) + "的群....")
            asf = await bot.group_list()
            # print(len(asf.data), asf.data)
            with open('config/autoSettings.yaml', 'r', encoding='utf-8') as f:
                result23 = yaml.load(f.read(), Loader=yaml.FullLoader)
            youquan1 = result23.get("trustGroups")
            totalquit = 0
            for nb in asf:
                gid = nb.id
                try:
                    sf = await bot.member_list(int(gid))
                    sf = len(sf.data)
                except Exception as e:
                    logger.error(e)
                    continue
                try:
                    if sf < setg and gid not in youquan1:
                        await bot.send_group_message(gid, "无授权小群，自动退出。")
                        logger.warning("已清退" + str(gid))
                        await bot.send(event, f"清退：{gid}")
                        await bot.quit(gid)
                except Exception as e:
                    logger.error(e)
                    continue
                    totalquit += 1
            await bot.send(event, "已退出" + str(totalquit) + "个群")
