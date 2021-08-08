import requests, base64
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


def generate_token():
    usrPass = "api@си:wZi1QsfD"
    b64Val = base64.b64encode(usrPass.encode()).decode()
    token = requests.post('https://online.moysklad.ru/api/remap/1.2/security/token', auth=('api@си'.encode('iso-8859-1'), 'wZi1QsfD'.encode('iso-8859-1'))).json()
    print(token)
    return token.get('access_token')

class FetchBarcodes(APIView):

    def post(self,request,**kwargs):
        token =  generate_token()
        headers = {"Authorization": f"Bearer {token}"}
        data = {}
        data['products'] = []

        return_list = request.data.get('codes')

        # for bar_code_founder in return_list:

        res5 = requests.get(f'https://online.moysklad.ru/api/remap/1.2/entity/assortment?filter=search={return_list}',
                            params=None, headers=headers).json()

        
        if res5.get('rows'):
            for new_bc in res5['rows']:
                if new_bc.get('barcodes'):
                    # this_variant_shtrix = []
                    for bar_c in new_bc['barcodes']:  
                        # this_variant_shtrix.append(list(bar_c.values())[0])                      
                        if list(bar_c.values())[0] ==  return_list:
                            data['products'].append({'id':new_bc.get('id'), "code" : list(bar_c.values())[0]})
                            break
                        else:
                            continue  
            if len(data['products']) and  len(data['products'][0].get('id')) > 0:
                data['is_modification'] = True
                return Response(data=data, status=200)
            else:
                data['products'] = []
                return Response(data=data, status=200)
        else:
            data['products'] = []
            return Response(data=data, status=200)         
  
        

class FetchProducts(APIView):
    """ We are fetching products from moysklad API 

    Example of request {'codes':['code1','code2']}
    
    """

    def post(self, request, **kwargs):
        global return_list
        token =  generate_token()
        headers = {"Authorization": f"Bearer {token}"}

        data = {}
        data['products'] = []
        if request.data.get('codes') and request.data.get('is_modification') == False:
            codes_list = request.data['codes']
            new_code_list = []
            iter_count = 0
            for i in codes_list:

                if not len(codes_list):
                    return
                if len(codes_list) == 1:
                    new_code_list.append(f'code={i}')
                if len(codes_list) > 1:

                    if iter_count == 0:
                        new_code_list.append(f'code={i};')
                    elif iter_count > 0 and iter_count < len(codes_list) - 1:
                        new_code_list[-1] += f'code={i};'
                    elif iter_count == len(codes_list) - 1:
                        new_code_list[-1] += f'code={i}'
                    iter_count += 1
            founded_codes = []
            res = requests.get(f'https://online.moysklad.ru/api/remap/1.2/entity/product/'
                               f'?filter={new_code_list[0]}', params=None, headers=headers).json()

            if res.get('rows'):
            # data['pr'] = res
                ct_code = 0
                for row in res['rows']:
                    ct_code += 1
                    if ct_code == 1:
                        founded_codes.append(f'code!={row.get("code")}')
                    else:
                        founded_codes[0]+=f'code!={row.get("code")}'
                    data['products'].append({'id': row['id'], 'code': row['code']})

            uncomitted_list = []
            if len(data['products']): 
                for i in list(data['products']):
                    uncomitted_list.append(str(i['code']).lower())

            return_list = []

            for i in codes_list:
                if i not in uncomitted_list:
                    return_list.append(str(i).lower())

            if len(return_list):
                my_variant = []
                ctr = 0
                if len(return_list) == 1:
                    my_variant.append(f'code={return_list[0]}')
                else:

                    for not_found_codes in return_list:
                        ctr += 1
                        if ctr == 1:
                            my_variant.append(f'code={not_found_codes}')
                        if ctr == len(return_list):
                            my_variant[0] += f'code={not_found_codes}'
                        else:
                            my_variant[0] += f'code={not_found_codes};'

                
                
                res2 = requests.get(
                    f'http://online.moysklad.ru/api/remap/1.2/entity/variant?filter=code={my_variant[0]}', params=None,
                    headers=headers).json()

                if res2.get('rows'):
                    ct_variant = 0
                    for i in res2['rows']:
                        ct_variant += 1
                        if len(founded_codes) == 0:
                            if ct_code == 1:
                                founded_codes.append(f'code!={i.get("code")}')
                            else:
                                founded_codes[0]+=f'code!={i.get("code")}'
                        else:
                            founded_codes[0]+=f'code!={i.get("code")}'
                        data['products'].append({'id': i.get('id'), "code": i.get('code'),'is_modification':True})
                        if str(i['code']).lower() in return_list:
                            return_list.remove(str(i['code']).lower())
    
                # if len(return_list):
                #     for not_code in return_list:
                #         res3 = requests.get(f'http://online.moysklad.ru/api/remap/1.2/entity/product?search={not_code}',
                #                             params=None, headers=headers).json()
                #         if res3.get('rows'):
                            
                #             data['products'].append(
                #                 {'id': res3.get('rows')[0].get('id'), "code": res3.get('rows')[0].get('code')})
                #             return_list.remove(not_code)
                # if len(return_list):
                #     for not_code_article in return_list:
                #         res4 = requests.get(
                #             f'http://online.moysklad.ru/api/remap/1.2/entity/product?filter=article={not_code_article}',
                #             params=None, headers=headers).json()
                #         if res4.get('rows'):
                            
                #             data['products'].append(
                #                 {'id': res4.get('rows')[0].get('id'), "code": res4.get('rows')[0].get('code')})
                #             return_list.remove(not_code)
        #         # data['is_modification'] = False
        # if request.data.get('is_modification') == True:
        #     if len(return_list):
                
        #         for bar_code_founder in return_list:

        #             res5 = requests.get(f'https://online.moysklad.ru/api/remap/1.2/entity/assortment?filter=search={bar_code_founder}',
        #                                 params=None, headers=headers).json()

        #             if res5.get('rows'):
        #                 for new_bc in res5['rows']:
        #                     if new_bc.get('barcodes'):
        #                         for bar_c in new_bc['barcodes']:
                                    
        #                             if list(bar_c.values())[0] in return_list:
        #                                 data['products'].append({'id':new_bc.get('id'), "code" : list(bar_c.values())[0]})
        #                                 return_list.remove(list(bar_c.values())[0])
        #         data['is_modification'] = True
                  

            code_error_dict = {}
            code_error_dict['code_errors'] = list()
            for i in return_list:
                code_error_dict['code_errors'].append(i)
            data['code_errors'] = code_error_dict['code_errors']
            return Response(data=data, status=200)
            


class FetchAgents(APIView):
    """ We are  fetching agent 
    
    Example of request {'name':'шебелян гаспар левонович'}
    
    """

    def post(self, request, **kwargs):
        token =  generate_token()
        headers = {"Authorization": f"Bearer {token}"}
        agents = request.data.get('name')
        res = requests.get(f'https://online.moysklad.ru/api/remap/1.2/entity/counterparty/'
                           f'?filter=name={agents}', params=None, headers=headers)
        data = res.json()
        return Response(data, status=200)


class FetchOrganization(APIView):
    """ Example of request {'inn':'5665656565','kpp':'55522555'} """

    def post(self, request, **kwargs):
        token =  generate_token()
        headers = {"Authorization": f"Bearer {token}"}
        organization_data = f'inn={request.data.get("inn")}&kpp={request.data.get("kpp")}'
        res = requests.get(f'https://online.moysklad.ru/api/remap/1.2/entity/organization/'
                           f'?filter={organization_data}', params=None, headers=headers)
        data = res.json()
        return Response(data, status=200)


class FetchStates(APIView):
    """ Example of request {"states": "OZON - Возврат" } """

    def post(self, request, **kwargs):

        token =  generate_token()
        headers = {"Authorization": f"Bearer {token}"}
        data_req = request.data
        res = requests.get('https://online.moysklad.ru/api/remap/1.2/entity/customerorder/metadata/', params=None,
                           headers=headers).json()

        counter = 0
        for st in res.get('states'):
            counter += 1
            if st['name'] == str(data_req['states']):

                data = {
                    'id': st['id'],
                    'name': st['name']
                }
                return Response(data=data, status=status.HTTP_200_OK)
            else:
                if counter < len(res.get('states')):
                    continue
                else:
                    data = {
                        'state_error': f'{data_req["states"][0]} is not defined'
                    }
                    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


class OrderForBuyer(APIView):
    """ Order for buyer 'Заказ покупателя' """

    def post(self, request, **kwargs):
        token =  generate_token()
        headers = {"Authorization": f"Bearer {token}"}
        data = request.data

        res = requests.post('https://online.moysklad.ru/api/remap/1.2/entity/customerorder', json=data, headers=headers)

        if res.status_code >= 200 and res.status_code <= 205:
            return Response(data=res.json(), status=status.HTTP_200_OK)
        return Response(data=res.json(), status=status.HTTP_400_BAD_REQUEST)


class FetchStore(APIView):
    """ Example of request {"store": 'Великий Новгород'} """

    def post(self, request, **kwargs):
        token =  generate_token()
        print(token)
        headers = {"Authorization": f"Bearer {token}"}
        store_name = request.data.get('store')
        res = requests.get(f'https://online.moysklad.ru/api/remap/1.2/entity/store/'
                           f'?filter=name={store_name}', params=None, headers=headers)
        print(res.json())
        data = {'id': res.json()['rows'][0]['id']}
        return Response(data=data, status=200)


class OrderSupplier(APIView):
    """ Order for buyer 'Заказ Поставщику'  required params name,organization,agent """

    def post(self, request, **kwargs):
        token =  generate_token()
        headers = {"Authorization": f"Bearer {token}"}
        data_req = request.data
        res = requests.post('https://online.moysklad.ru/api/remap/1.2/entity/purchaseorder',
                            json=data_req, headers=headers)
        if res.status_code >= 200 and res.status_code <= 205:
            return Response(data=res.json(), status=status.HTTP_200_OK)
        return Response(data=res.json(), status=status.HTTP_400_BAD_REQUEST)


class OrderAcceptance(APIView):
    """ Приемка required params name,organization,agent,store """

    def post(self, request, **kwargs):
        token =  generate_token()
        headers = {"Authorization": f"Bearer {token}"}
        data_req = request.data
        res = requests.post('https://online.moysklad.ru/api/remap/1.2/entity/supply',
                            json=data_req, headers=headers)
        if res.status_code >= 200 and res.status_code <= 205:
            return Response(data=res.json(), status=status.HTTP_200_OK)
        return Response(data=res.json(), status=status.HTTP_400_BAD_REQUEST)


class OrderShipments(APIView):
    """ Отгрузки  required params name,organization,agent,store """

    def post(self, request, **kwargs):
        token =  generate_token()
        headers = {"Authorization": f"Bearer {token}"}
        data_req = request.data
        res = requests.post('https://online.moysklad.ru/api/remap/1.2/entity/demand',
                            json=data_req, headers=headers)
        if res.status_code >= 200 and res.status_code <= 205:
            return Response(data=res.json(), status=status.HTTP_200_OK)
        return Response(data=res.json(), status=status.HTTP_400_BAD_REQUEST)
