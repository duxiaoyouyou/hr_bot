from move_sap_info_extractor import extractor, move_sap_selling_info
import move_sap_calculator
import json
import logging
logger = logging.getLogger("qa_bot.py")

class qa_bot:

    def __init__(self, openai):
        self.openai = openai
        self.extractor = extractor(openai)
        self.system_message = "你是一个AI助手，专门回答关于MoveSAP股票相关的问题。" \
                              "MoveSAP是SAP公司给优秀员工股票的一种嘉奖方式。" \
                              "通常情况下，在公司发放给员工股票的同时，就需要卖掉其中的一部分用来为员工缴纳相关的个人所得税。" \
                              "在每次面对提问时，我都会给你一个关于当前员工收入MoveSap股票的详细计算过程以帮助你正确回答问题。"


    def ask_by_calculation(self, query):
        infoStr = self.extractor.extract(query)
        logger.info(f"Selling info: {infoStr}")
        infoJson = json.loads(infoStr)
        selling_info = move_sap_selling_info(infoJson)
        if selling_info.errorCode:
            return {"query": query,
                    "response": "抱歉，我们需要如下信息来回答您的问题\n"
                                "1. 员工获得的move sap数额\n"
                                "2. move sap售卖当天的汇率\n"
                                "3. move sap售卖当天的股价\n"
                                "4. 售出股票到花旗银行当天的汇率\n"
                                "5. 售出股票当月员工的个人所得税税率"}
        calculator = move_sap_calculator.calculator(selling_info.stockQuantity,
                                selling_info.saleExRate,
                                selling_info.stockPrice,
                                selling_info.actualTaxRate,
                                selling_info.transferExRate,
                                selling_info.maxTaxRate)
        calculator.calculate()
        calculation_detail = calculator.to_calculation_details()
        logger.info(f"Calculation detail: {calculation_detail}")
        query = f"员工的问题是：\n {query} \n" \
                f"以下是这次Move SAP股票的相关计算信息： \n {calculation_detail} "
        response = self.openai.ChatCompletion.create(
            engine="gpt-4",
            messages=[
                {"role": "system", "content": self.system_message},
                {"role": "user", "content": query}
            ],
            temperature=0
        )
        logger.info(f"Query: {query}")
        return {"query": query, "response": response["choices"][0]["message"]["content"]}

    def ask(self, query, message_history):
        messages_for_ask = [
                {"role": "system", "content": self.system_message}
            ]
        messages_for_ask.extend(message_history)
        messages_for_ask.append({"role": "user", "content": query})
        logger.info(f"Messages: {messages_for_ask}")
        response = self.openai.ChatCompletion.create(
            engine="gpt-4",
            messages=messages_for_ask,
            temperature=0
        )
        return response["choices"][0]["message"]["content"]





