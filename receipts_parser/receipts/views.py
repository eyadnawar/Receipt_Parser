from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core import serializers
from .serializers import *
from datetime import datetime
import re
import json
from django.forms.models import model_to_dict
import os
from io import BytesIO
import uuid
from .file_parser import *

from django.conf import settings
from django.core.files import uploadedfile
from django.core.files.base import File

# Create your views here.

@api_view(['POST'])
def addReceipt(request):
    # print(request.data)
    # print(request.data['file'])
    serializer = ReceiptsSerializer(data=request.data)
    if(serializer.is_valid()):

        receipt_id = str(uuid.uuid1().int)    ## create a uuid for the receipt id
        receipt = request.data['file']     ## the file object (InMemoryUploadedFile object)
        #receipt = uploadedfile.InMemoryUploadedFile.open(request.data['file']).readlines()
        receipt_name = str(request.data['file'])  ## the name of the receipt
        big_list = file_parser(file=uploadedfile.InMemoryUploadedFile.open(request.data['file']).readlines(),
                               delimiter='-')   ## get the list of lists representing each block
        num_of_blocks = get_num_of_blocks(big_list)  ## get the number of blocks
        receipt_blocks = get_border(big_list)   ## get the border of each block

        receipt_to_save = Receipts(
            receipt_id=receipt_id,
            receipt=receipt,
            receipt_name=receipt_name,
            num_of_blocks=num_of_blocks,
            receipt_blocks=receipt_blocks
        )

        #print(receipt_to_save)
        #receipt_to_save.save()         ## save the receipts object to the mongodb

        print(receipt)

        return Response({
            "message": "success",
            "Receipt_details": {
                "receipt_id": receipt_id,
                "receipt": receipt,
                "receipt_nme": receipt_name,
                "num_of_blocks": num_of_blocks,
                "receipt_blocks": receipt_blocks
            },
            "status": 200
        })

    else:
        return Response({
            "message": "request is invalid, please try again",
            "status": 500
        })
