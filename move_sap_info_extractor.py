# import openai
# import json
import logging
logger = logging.getLogger("extractor.py")
class extractor:

    def __init__(self, openai):
        self.openai = openai

    def extract(self, question):
        checkPrompt = f"Please check if all the below 5 info can be parsed from the question\n " \
                      f"1. the stock quantity to be sold\n" \
                      f"2. stock selling day price\n " \
                      f"3. exchange rate at stock selling date\n" \
                      f"4. exchange rate when bank received the cash amount\n" \
                      f"5. actual income tax rate\n" \
                      f"Return 0 if any of the info is missing, " \
                      f"return 1 if all of above info can be parsed from the question.\n" \
                      f"Question {question}"
        response = self.openai.ChatCompletion.create(
            engine="gpt-4",
            messages=[
                {"role": "user", "content": "员工a有1000股，卖掉的时候汇率为7"},
                {"role": "assistant", "content": '0'},
                {"role": "user", "content": "Freya，你准备一下，有位中国同事拿到了1000股公司股票，"
                                            "8/13卖掉的时候股价好像是正好10块，汇率是7，花旗那边8/14收到钱，当时的汇率是6.9"
                                            "这位同事实际纳税比例应该是20%"},
                {"role": "assistant", "content": '1'},

                {"role": "user", "content": checkPrompt},
            ],
            temperature=0
        )
        response = response["choices"][0]["message"]["content"]
        isInfoComplete = bool(int(response))
        if isInfoComplete:
            query = f"Please parse the stock quantity to be sold, stock selling day price, " \
                    f"exchange rate at stock selling date, " \
                    f"exchange rate when bank received the cash amount, " \
                    f"income tax rate upperbound and actual income tax rate from the question into " \
                    f"json with stockQuantity as key for stock quantity to be sold, " \
                    f"stockPrice as the key for stock selling day price, saleExRate as exchange rate " \
                    f"at stock selling date," \
                    f"actualTaxRate as the key for actual income tax rate, transferExRate as the key for " \
                    f"exchange rate when bank received the cash amount and the maxTaxRate as the key for " \
                    f"income tax rate upperbound. " \
                    f"In the output json" \
                    f"1. If the income tax rate upperbound is not given, " \
                    f"0.45 should be used as the default value.\n " \
                    f"2. All the rate should be converted to a float value." \
                    f"For example, if 20% is given it should be converted to 0.2 instead.\n" \
                    f"3. Stock price and exchange rates should be converted into the format of number.\n" \
                    f"4. For errorHandling purpose set errorCode to 0 in the output json " \
                    f"\n Question: {str(question)} "
            response = self.openai.ChatCompletion.create(
                engine="gpt-4",
                messages=[
                    {"role": "user", "content": "Freya，你准备一下，有位中国同事拿到了1000股公司股票，"
                                                "8/13卖掉的，股价好像是正好10块，汇率是7，花旗那边8/14收到钱，当时的汇率是6.9"
                                                "这位同事实际纳税比例应该是20%"},
                    {"role": "assistant", "content": '{"errorCode": 0, "stockQuantity": 1000, "stockPrice": 10, '
                                                     '"saleExRate": 7, "actualTaxRate": 0.2, "transferExRate": 6.9, '
                                                     '"maxTaxRate": 0.45}'},

                    {"role": "user", "content": query},
                ],
                temperature=0
            )
            return response["choices"][0]["message"]["content"]
        else:
            return '{"errorCode": 1}'



class move_sap_selling_info:
    def __init__(self, dict):
        self.errorCode = bool(int(dict['errorCode']))
        logger.info(f"dict {dict}")
        if not self.errorCode:
            self.stockQuantity = float(dict['stockQuantity'])
            self.stockPrice = float(dict['stockPrice'])
            self.saleExRate = float(dict['saleExRate'])
            self.actualTaxRate = float(dict['actualTaxRate'])
            self.transferExRate = float(dict['transferExRate'])
            self.maxTaxRate = float(dict['maxTaxRate'])
