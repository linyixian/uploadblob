import cv2
from datetime import datetime
from azure.storage.blob import BlobServiceClient,BlobClient,ContainerClient

container_name='localblobstorage'
local_name='tmp.jpg'

cn_string='DefaultEndpointsProtocol=http;BlobEndpoint=http://localhost:11002/<account name>;AccountName=<account name>;AccountKey=<account key>;'

serviceClient=BlobServiceClient.from_connection_string(cn_string)

cap=cv2.VideoCapture(0)

t_=-1

print("Start!")

while True:
    if cv2.waitKey(1)==13:
        break

    ret,frame=cap.read()

    d=datetime.now()
    t=d.minute

    if t_ != t:
        cv2.imwrite("tmp.jpg",frame)
        blob_name=d.strftime("%Y%m%d%H%M")+".jpg"
        blobClient=serviceClient.get_blob_client(container_name,blob=blob_name)
        with open(local_name,'rb') as data:
            blobClient.upload_blob(data)

        print(d.strftime("%Y%m%d%H%M"))
        t_=t
    cv2.imshow("frame",frame)

print("Stop!")
cap.release()
cv2.destroyAllWindows()
