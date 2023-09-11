# import openai
# import json

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
            engine="gpt-35-turbo",
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
        print(response)
        isInfoComplete = bool(int(response))
        print(isInfoComplete)
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
                    f"3. Only the integer part of the stock price or exchange rate should be retained.\n" \
                    f"4. For errorHandling purpose set errorCode to 0 in the output json " \
                    f"\n Question: {str(question)} "
            response = self.openai.ChatCompletion.create(
                engine="gpt-35-turbo",
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
        if not self.errorCode:
            self.stockQuantity = int(dict['stockQuantity'])
            self.stockPrice = int(dict['stockPrice'])
            self.saleExRate = float(dict['saleExRate'])
            self.actualTaxRate = float(dict['actualTaxRate'])
            self.transferExRate = float(dict['transferExRate'])
            self.maxTaxRate = float(dict['maxTaxRate'])

# openai.api_key = "9f32e291dbd248c2b4372647bd937577"
# openai.api_base = "https://miles-playground.openai.azure.com"
# openai.api_type = "azure"
# openai.api_version = "2023-03-15-preview"
# extracotr = extractor(openai)
# infoStr = extracotr.extract("max 有1000股需要行权，8/13卖掉的时候股价好像是10块，当天的汇率是7.1，"
#                             "花旗那边10/14收到钱，收到那天的汇率是7.0"
#                             "这位同事实际纳税比例应该是30%")
# print(infoStr)
# infoStr = extracotr.extract("max有1000股，卖掉的时候汇率为7")
#
# print(json.loads(infoStr))
# info = move_sap_selling_info(json.loads(infoStr))
# print(info)
# print(info.errorCode)